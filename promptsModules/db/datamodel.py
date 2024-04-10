from sqlite3 import Connection, connect
from enum import Enum
from typing import Dict, List, Optional, TypedDict, Tuple
from promptsModules.db.tool import (
    cwd,
    get_modified_date,
    human_readable_size,
    tags_translate,
    is_dev,
    find,
    unique_by,
)
from contextlib import closing
import os
import threading
import re


class FileInfoDict(TypedDict):
    type: str
    date: float
    size: int
    name: str
    bytes: bytes
    created_time: float
    fullpath: str


class Cursor:
    def __init__(self, has_next=True, next=""):
        self.has_next = has_next
        self.next = next


class DataBase:
    local = threading.local()

    _initing = False

    reConnect = False

    num = 0

    path = "tags.db"

    @classmethod
    def get_conn(clz) -> Connection:
        print("reConnect", clz.reConnect)
        # for : sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread
        if hasattr(clz.local, "conn") and clz.reConnect is False:
            return clz.local.conn
        else:
            conn = clz.init()
            clz.local.conn = conn
            clz.reConnect = False

            return conn

    @classmethod
    def init(clz):
        # Create a connection and open the database
        conn = connect(
            clz.path if os.path.isabs(clz.path) else os.path.join(cwd, clz.path)
        )

        def regexp(expr, item):
            if not isinstance(item, str):
                return False
            reg = re.compile(expr, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
            return reg.search(item) is not None

        conn.create_function("regexp", 2, regexp)
        try:
            Folder.create_table(conn)
            ImageTag.create_table(conn)
            Tag.create_table(conn)
            Image.create_table(conn)
            ExtraPath.create_table(conn)
            TrainTag.create_table(conn)
            TrainImageTags.create_table(conn)
        finally:
            conn.commit()
        clz.num += 1
        if is_dev:
            print(f"Current connection number{clz.num}")
        return conn


class Image:
    def __init__(self, path, exif=None, pos_prompt="", size=0, date="", id=None):
        self.path = path
        self.exif = exif
        self.pos_prompt = pos_prompt
        self.id = id
        self.size = size
        self.date = date

    def to_file_info(self) -> FileInfoDict:
        return {
            "type": "file",
            "id": self.id,
            "date": self.date,
            "created_date": self.date,
            "size": human_readable_size(self.size),
            "is_under_scanned_path": True,
            "bytes": self.size,
            "name": os.path.basename(self.path),
            "fullpath": self.path,
            "posPrompt": self.pos_prompt,
        }

    def save(self, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                "INSERT OR REPLACE  INTO image (path, exif, pos_prompt, size, date) VALUES (?, ?, ?, ?, ?)",
                (self.path, self.exif, self.pos_prompt, self.size, self.date),
            )
            self.id = cur.lastrowid

    def update_path(self, conn: Connection, new_path: str):
        self.path = os.path.normpath(new_path)
        with closing(conn.cursor()) as cur:
            cur.execute("UPDATE image SET path = ? WHERE id = ?", (self.path, self.id))

    @classmethod
    def get(cls, conn: Connection, id_or_path):
        with closing(conn.cursor()) as cur:
            cur.execute(
                "SELECT * FROM image WHERE id = ? OR path = ?", (id_or_path, id_or_path)
            )
            row = cur.fetchone()
            if row is None:
                return None
            else:
                return cls.from_row(row)

    @classmethod
    def get_by_ids(cls, conn: Connection, ids: List[int]) -> List["Image"]:
        if not ids:
            return []

        query = """
            SELECT * FROM image
            WHERE id IN ({})
        """.format(
            ",".join("?" * len(ids))
        )

        with closing(conn.cursor()) as cur:
            cur.execute(query, ids)
            rows = cur.fetchall()

        images = []
        for row in rows:
            images.append(cls.from_row(row))
        return images

    @classmethod
    def create_table(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS image (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            path TEXT UNIQUE,
                            exif TEXT,
                            pos_prompt TEXT,
                            size INTEGER,
                            date TEXT
                        )"""
            )
            cur.execute("CREATE INDEX IF NOT EXISTS image_idx_path ON image(path)")

    @classmethod
    def count(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT COUNT(*) FROM image")
            count = cur.fetchone()[0]
            return count

    @classmethod
    def from_row(cls, row: tuple):
        image = cls(path=row[1], exif=row[2], pos_prompt=row[3], size=row[4], date=row[5])
        image.id = row[0]
        return image

    @classmethod
    def simple_from_row(cls, row: tuple):
        image = cls(path="", pos_prompt=row[1], date=row[2], exif=row[3])
        image.id = row[0]
        return image

    @classmethod
    def remove(cls, conn: Connection, image_id: int) -> None:
        with closing(conn.cursor()) as cur:
            cur.execute("DELETE FROM image WHERE id = ?", (image_id,))
            conn.commit()

    @classmethod
    def safe_batch_remove(cls, conn: Connection, image_ids: List[int]) -> None:
        if not (image_ids):
            return
        with closing(conn.cursor()) as cur:
            try:
                placeholders = ",".join("?" * len(image_ids))
                cur.execute(
                    f"DELETE FROM image_tag WHERE image_id IN ({placeholders})",
                    image_ids,
                )
                cur.execute(
                    f"DELETE FROM image WHERE id IN ({placeholders})", image_ids
                )
            except BaseException as e:
                print(e)
            finally:
                conn.commit()

    @classmethod
    def find_by_substring(
        cls, conn: Connection, substring: str, limit: int = 500, cursor="", regexp="", from_exif=False,
    ) -> Tuple[List["Image"], str]:
        api_cur = Cursor()
        with closing(conn.cursor()) as cur:
            params = []
            where_clauses = []
            if regexp:
                where_clauses.append("(exif REGEXP ?)")
                params.append(regexp)
            if from_exif:
                where_clauses.append("(exif LIKE ?)")
                params.append(f"%{substring}%")
            else:
                where_clauses.append("(path LIKE ? OR pos_prompt LIKE ?)")
                params.extend((f"%{substring}%", f"%{substring}%"))
            if cursor:
                where_clauses.append("(date < ?)")
                params.append(cursor)
            sql = "SELECT id, pos_prompt, date, exif FROM image"
            if where_clauses:
                sql += " WHERE "
                sql += " AND ".join(where_clauses)
            sql += " ORDER BY date DESC LIMIT ? "
            params.append(limit)
            cur.execute(sql, params)
            rows = cur.fetchall()

        api_cur.has_next = len(rows) >= limit
        images = []
        for row in rows:
            img = cls.simple_from_row(row)
            images.append(img)

        cursor_date = None
        if images:
            api_cur.next = str(images[-1].date)
            cursor_date = str(images[-1].date)
        return images, cursor_date

class TrainImageTags:
    def __init__(self, tain_tag_id: str, tags_info: str):
        self.tain_tag_id = tain_tag_id
        self.tags_info = tags_info
        self.id = None

    @classmethod
    def create_table(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS train_image_tags (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            tain_tag_id TEXT,
                            tags_info TEXT
                        )"""
            )
            cur.execute("CREATE INDEX IF NOT EXISTS train_image_tags_idx_tain_tag_id ON train_image_tags(tain_tag_id)")
            cur.execute("PRAGMA table_info(train_image_tags)")

    @classmethod
    def saveTags(cls, conn, tain_tag_id, tags_info: List[str]):
        with closing(conn.cursor()) as cur:
            # find if tain_tag_id has relate data, if have, delete all
            cur.execute(
                "SELECT * FROM train_image_tags WHERE tain_tag_id = ?", (tain_tag_id,)
            )
            rows = cur.fetchall()
            if rows:
                cur.execute(
                    "DELETE FROM train_image_tags WHERE tain_tag_id = ?", (tain_tag_id,)
                )
                conn.commit()

            # loop and insert all
            for tag in tags_info:
                cur.execute(
                    "INSERT INTO train_image_tags (tain_tag_id, tags_info) VALUES (?, ?)",
                    (tain_tag_id, tag),
                )
            conn.commit()

    @classmethod
    def getAllTags(cls, conn, tain_tag_id):
        with closing(conn.cursor()) as cur:
            cur.execute(
                "SELECT * FROM train_image_tags WHERE tain_tag_id = ?", (tain_tag_id,)
            )
            rows = cur.fetchall()
            tags: list[str] = []
            for row in rows:
                tags.append(row[2])
            return tags

class TrainTag:
    def __init__(self, model_name: str, tags_info: str, comments: str = ""):
        self.model_name = model_name
        self.tags_info = tags_info
        self.comments = comments
        self.id = None

    @classmethod
    def create_table(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS train_tag (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            model_name TEXT UNIQUE,
                            tags_info TEXT
                        )"""
            )
            cur.execute("CREATE INDEX IF NOT EXISTS train_tag_idx_model_name ON train_tag(model_name)")
            cur.execute("PRAGMA table_info(train_tag)")
            columns = [column[1] for column in cur.fetchall()]

            if "comments" not in columns:
                cur.execute("ALTER TABLE train_tag ADD COLUMN comments TEXT DEFAULT ''")

    def save(self, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                "INSERT OR REPLACE  INTO train_tag (model_name, tags_info, comments) VALUES (?, ?, ?)",
                (self.model_name, self.tags_info, self.comments),
            )
            conn.commit()
            self.id = cur.lastrowid

    def update_comments(self, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                "UPDATE train_tag SET comments = ? WHERE model_name = ?",
                (self.comments, self.model_name),
            )
            conn.commit()

    @classmethod
    def get(cls, conn: Connection, model_name):
        with closing(conn.cursor()) as cur:
            cur.execute(

                "SELECT * FROM train_tag WHERE model_name LIKE ? ", (f"%{model_name}%",)
            )
            row = cur.fetchone()
            if row is None:
                return None
            else:
                return cls.from_row(row)

    @classmethod
    def get_all(cls, conn: Connection):
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM train_tag")
            rows = cur.fetchall()
            train_tags: list[TrainTag] = []
            for row in rows:
                train_tags.append(cls.from_row(row))
            return train_tags

    @classmethod
    def from_row(cls, row: tuple):
        train_tag = cls(model_name=row[1], tags_info=row[2])
        train_tag.id = row[0]
        train_tag.comments = row[3]
        return train_tag

    @classmethod
    def remove(cls, conn: Connection, model_name):
        with closing(conn.cursor()) as cur:
            cur.execute("DELETE FROM train_tag WHERE model_name = ?", (model_name,))
            conn.commit()

class Tag:
    def __init__(self, name: str, score: int, type: str, count=0):
        self.name = name
        self.score = score
        self.type = type
        self.count = count
        self.id = None
        self.display_name = tags_translate.get(name)

    def save(self, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                "INSERT OR REPLACE INTO tag (id, name, score, type, count) VALUES (?, ?, ?, ?, ?)",
                (self.id, self.name, self.score, self.type, self.count),
            )
            self.id = cur.lastrowid

    @classmethod
    def remove(cls, conn, tag_id):
        with closing(conn.cursor()) as cur:
            cur.execute("DELETE FROM tag WHERE id = ?", (tag_id,))
            conn.commit()

    @classmethod
    def remove_by_name(cls, conn, tag_name):
        with closing(conn.cursor()) as cur:
            cur.execute("DELETE FROM tag WHERE name = ?", (tag_name,))
            conn.commit()

    @classmethod
    def get(cls, conn: Connection, id):
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM tag WHERE id = ?", (id,))
            row = cur.fetchone()
            if row is None:
                return None
            else:
                return cls.from_row(row)

    @classmethod
    def get_all_custom_tag(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM tag where type = 'custom'")
            rows = cur.fetchall()
            tags: list[Tag] = []
            for row in rows:
                tags.append(cls.from_row(row))
            return tags

    @classmethod
    def get_all_lora_tag(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM tag where type = 'lora' ORDER BY count DESC, score DESC")
            rows = cur.fetchall()
            tags: list[Tag] = []
            for row in rows:
                tags.append(cls.from_row(row))
            return tags

    @classmethod
    def get_all_lyco_tag(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM tag where type = 'lyco' ORDER BY count DESC")
            rows = cur.fetchall()
            tags: list[Tag] = []
            for row in rows:
                tags.append(cls.from_row(row))
            return tags

    @classmethod
    def update_tag_score(cls, conn, tag, score):
        with closing(conn.cursor()) as cur:
            cur.execute("UPDATE tag SET score = ? WHERE name = ?", (score, tag))
            conn.commit()

    @classmethod
    def get_all_model_tags(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM tag where (type = 'lora' OR type = 'lyco') ORDER BY count DESC")
            rows = cur.fetchall()
            tags: list[Tag] = []
            for row in rows:
                tags.append(cls.from_row(row))

            cur.execute(
                """
                SELECT * FROM tag
                WHERE type = 'pos'
                    AND name NOT IN ('best quality', 'absurdres', 'ultra detailed', 'masterpiece')
                ORDER BY count DESC
                LIMIT 256
                """
            )
            second_query_rows = cur.fetchall()
            for row in second_query_rows:
                tags.append(cls.from_row(row))

            return tags

    @classmethod
    def get_all(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM tag")
            rows = cur.fetchall()
            tags: list[Tag] = []
            for row in rows:
                tags.append(cls.from_row(row))
            return tags

    @classmethod
    def get_or_create(cls, conn: Connection, name: str, type: str):
        assert name and type
        with closing(conn.cursor()) as cur:
            cur.execute(
                "SELECT tag.* FROM tag WHERE name = ? and type = ?", (name, type)
            )
            row = cur.fetchone()
            if row is None:
                tag = cls(name=name, score=0, type=type)
                tag.save(conn)
                return tag
            else:
                return cls.from_row(row)

    @classmethod
    def from_row(cls, row: tuple):
        tag = cls(name=row[1], score=row[2], type=row[3], count=row[4])
        tag.id = row[0]
        return tag

    @classmethod
    def create_table(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS tag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            score INTEGER,
            type TEXT,
            count INTEGER,
            UNIQUE(name, type) ON CONFLICT REPLACE
            );
            """
            )
            cur.execute("CREATE INDEX IF NOT EXISTS tag_idx_name ON tag(name)")
            cur.execute(
                """INSERT OR IGNORE INTO tag(name, score, type, count)
                VALUES ("like", 0, "custom", 0);
                """
            )


class ImageTag:
    def __init__(self, image_id: int, tag_id: int):
        assert tag_id and image_id
        self.image_id = image_id
        self.tag_id = tag_id

    def save(self, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO image_tag (image_id, tag_id) VALUES (?, ?)",
                (self.image_id, self.tag_id),
            )

    def save_or_ignore(self, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                "INSERT OR IGNORE INTO image_tag (image_id, tag_id) VALUES (?, ?)",
                (self.image_id, self.tag_id),
            )

    @classmethod
    def get_tags_for_image(
        cls,
        conn: Connection,
        image_id: int,
        tag_id: Optional[int] = None,
        type: Optional[str] = None,
    ):
        with closing(conn.cursor()) as cur:
            query = "SELECT tag.* FROM tag INNER JOIN image_tag ON tag.id = image_tag.tag_id WHERE image_tag.image_id = ?"
            params = [image_id]
            if tag_id:
                query += " AND image_tag.tag_id = ?"
                params.append(tag_id)
            if type:
                query += " AND tag.type = ?"
                params.append(type)
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            return [Tag.from_row(x) for x in rows]

    @classmethod
    def get_images_for_tag(cls, conn: Connection, tag_id):
        with closing(conn.cursor()) as cur:
            cur.execute(
                "SELECT image.* FROM image INNER JOIN image_tag ON image.id = image_tag.image_id WHERE image_tag.tag_id = ?",
                (tag_id,),
            )
            rows = cur.fetchall()
            images = []
            for row in rows:
                images.append(Image.from_row(row))
            return images

    @classmethod
    def create_table(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS image_tag (
                            image_id INTEGER,
                            tag_id INTEGER,
                            FOREIGN KEY (image_id) REFERENCES image(id),
                            FOREIGN KEY (tag_id) REFERENCES tag(id),
                            PRIMARY KEY (image_id, tag_id)
                        )"""
            )

    @classmethod
    def get_images_by_tags(
        cls,
        conn: Connection,
        tag_dict: Dict[str, List[int]],
        limit: int = 500,
        cursor="",
        folder_paths: List[str] = None,
    ) -> Tuple[List[Image], Cursor]:
        query = """
            SELECT image.id, image.path, image.size,image.date
            FROM image
            INNER JOIN image_tag ON image.id = image_tag.image_id
        """

        where_clauses = []
        params = []

        for operator, tag_ids in tag_dict.items():
            if operator == "and" and tag_dict["and"]:
                where_clauses.append(
                    "tag_id IN ({})".format(",".join("?" * len(tag_ids)))
                )
                params.extend(tag_ids)
            elif operator == "not" and tag_dict["not"]:
                where_clauses.append(
                    """(image_id NOT IN (
  SELECT image_id
  FROM image_tag
  WHERE tag_id IN ({})
))""".format(
                        ",".join("?" * len(tag_ids))
                    )
                )
                params.extend(tag_ids)
            elif operator == "or" and tag_dict["or"]:
                where_clauses.append(
                    """(image_id IN (
  SELECT image_id
  FROM image_tag
  WHERE tag_id IN ({})
  GROUP BY image_id
  HAVING COUNT(DISTINCT tag_id) >= 1
)
)""".format(
                        ",".join("?" * len(tag_ids))
                    )
                )
                params.extend(tag_ids)    

        if folder_paths:
            folder_clauses = []
            for folder_path in folder_paths:
                folder_clauses.append("(image.path LIKE ?)")
                params.append(os.path.join(folder_path, "%"))
                print(folder_path)
            where_clauses.append("(" + " OR ".join(folder_clauses) + ")")

        if cursor:
            where_clauses.append("(image.date < ?)")
            params.append(cursor)
        if where_clauses:
            query += " WHERE " + " AND ".join(where_clauses)
        query += " GROUP BY image.id"
        if "and" in tag_dict and tag_dict['and']:
            query += " HAVING COUNT(DISTINCT tag_id) = ?"
            params.append(len(tag_dict["and"]))

        query += " ORDER BY date DESC LIMIT ?"
        params.append(limit)
        api_cur = Cursor()
        with closing(conn.cursor()) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            images = []
            for row in rows:
                img = Image(id=row[0], path=row[1], size=row[2], date=row[3])
                images.append(img)
            api_cur.has_next = len(rows) >= limit
            if images:
                api_cur.next = str(images[-1].date)
            return images, api_cur

    @classmethod
    def batch_get_tags_by_path(
        cls, conn: Connection, paths: List[str], type="custom"
    ) -> Dict[str, List[Tag]]:
        if not paths:
            return {}
        tag_dict = {}
        with closing(conn.cursor()) as cur:
            placeholders = ",".join("?" * len(paths))
            query = f"""
                SELECT image.path, tag.* FROM image_tag
                INNER JOIN image ON image_tag.image_id = image.id
                INNER JOIN tag ON image_tag.tag_id = tag.id
                WHERE tag.type = '{type}' AND image.path IN ({placeholders})
            """
            cur.execute(query, paths)
            rows = cur.fetchall()
            for row in rows:
                path = row[0]
                tag = Tag.from_row(row[1:])
                if path in tag_dict:
                    tag_dict[path].append(tag)
                else:
                    tag_dict[path] = [tag]
        return tag_dict

    @classmethod
    def remove(
        cls,
        conn: Connection,
        image_id: Optional[int] = None,
        tag_id: Optional[int] = None,
    ) -> None:
        assert image_id or tag_id
        with closing(conn.cursor()) as cur:
            if tag_id and image_id:
                cur.execute(
                    "DELETE FROM image_tag WHERE image_id = ? and tag_id = ?",
                    (image_id, tag_id),
                )
            elif tag_id:
                cur.execute("DELETE FROM image_tag WHERE tag_id = ?", (tag_id,))
            else:
                cur.execute("DELETE FROM image_tag WHERE image_id = ?", (image_id,))
            conn.commit()


class Folder:
    def __init__(self, id: int, path: str, modified_date: str):
        self.id = id
        self.path = path
        self.modified_date = modified_date

    @classmethod
    def create_table(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS folders
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        path TEXT,
                        modified_date TEXT)"""
            )
            cur.execute("CREATE INDEX IF NOT EXISTS folders_idx_path ON folders(path)")

    @classmethod
    def check_need_update(cls, conn: Connection, folder_path: str):
        folder_path = os.path.normpath(folder_path)
        with closing(conn.cursor()) as cur:
            if not os.path.exists(folder_path):
                return False
            cur.execute("SELECT * FROM folders WHERE path=?", (folder_path,))
            folder_record = cur.fetchone()  # If this folder is not recorded, or the modification time is different from the database, you need to modify
            return not folder_record or (
                folder_record[2] != get_modified_date(folder_path)
            )

    @classmethod
    def update_modified_date_or_create(cls, conn: Connection, folder_path: str):
        folder_path = os.path.normpath(folder_path)
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM folders WHERE path = ?", (folder_path,))
            row = cur.fetchone()
            if row:
                cur.execute(
                    "UPDATE folders SET modified_date = ? WHERE path = ?",
                    (get_modified_date(folder_path), folder_path),
                )
            else:
                cur.execute(
                    "INSERT INTO folders (path, modified_date) VALUES (?, ?)",
                    (folder_path, get_modified_date(folder_path)),
                )

    @classmethod
    def get_expired_dirs(cls, conn: Connection):
        dirs: List[str] = []
        with closing(conn.cursor()) as cur:
            cur.execute("SELECT * FROM folders")
            result_set = cur.fetchall()
            extra_paths = ExtraPath.get_extra_paths(conn)
            for ep in extra_paths:
                if not find(result_set, lambda x: x[1] == ep.path):
                    dirs.append(ep.path)
            for row in result_set:
                folder_path = row[1]
                if (
                    os.path.exists(folder_path)
                    and get_modified_date(folder_path) != row[2]
                ):
                    dirs.append(folder_path)
            return unique_by(dirs, os.path.normpath)

    @classmethod
    def remove_folder(cls, conn: Connection, folder_path: str):
        folder_path = os.path.normpath(folder_path)
        with closing(conn.cursor()) as cur:
            cur.execute("DELETE FROM folders WHERE path = ?", (folder_path,))


class ExtraPathType(Enum):
    scanned = "scanned"
    walk = "walk"
    cli_only = "cli_access_only"


class ExtraPath:
    def __init__(self, path: str, type: Optional[ExtraPathType] = None):
        assert type
        self.path = os.path.normpath(path)
        self.type = type

    def save(self, conn):
        assert self.type in [ExtraPathType.walk, ExtraPathType.scanned]
        with closing(conn.cursor()) as cur:
            cur.execute(
                "INSERT INTO extra_path (path, type) VALUES (?, ?) ON CONFLICT (path) DO UPDATE SET type = ?",
                (self.path, self.type.value, self.type.value),
            )

    @classmethod
    def get_extra_paths(
        cls, conn, type: Optional[ExtraPathType] = None
    ) -> List["ExtraPath"]:
        query = "SELECT * FROM extra_path"
        params = ()
        if type:
            query += " WHERE type = ?"
            params = (type.value,)
        with closing(conn.cursor()) as cur:
            cur.execute(query, params)
            rows = cur.fetchall()
            paths: List[ExtraPath] = []
            for row in rows:
                path = row[0]
                if os.path.exists(path):
                    paths.append(ExtraPath(path, ExtraPathType(row[1])))
                # else:
                #     cls.remove(conn, path)
            return paths

    @classmethod
    def remove(
        cls,
        conn,
        path: str,
        type: Optional[ExtraPathType] = None,
        img_search_dirs: Optional[List[str]] = [],
    ):
        with closing(conn.cursor()) as cur:
            sql = "DELETE FROM extra_path WHERE path = ?"
            path = os.path.normpath(path)
            cur.execute(sql, (path,))
            if path not in img_search_dirs:
                Folder.remove_folder(conn, path)
            conn.commit()

    @classmethod
    def create_table(cls, conn):
        with closing(conn.cursor()) as cur:
            cur.execute(
                """CREATE TABLE IF NOT EXISTS extra_path (
                            path TEXT PRIMARY KEY,
                            type TEXT NOT NULL
                        )"""
            )
