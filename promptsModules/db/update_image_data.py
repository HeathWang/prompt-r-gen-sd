from contextlib import closing
from typing import Dict, List
from promptsModules.db.datamodel import Image as DbImg, Tag, ImageTag, DataBase, Folder
import os
from PIL import Image
from promptsModules.db.tool import (
    read_sd_webui_gen_info_from_image,
    parse_generation_parameters,
    is_valid_image_path,
    get_modified_date,
    is_dev,
)


# Define a function to obtain the EXIF data of the picture file
def get_exif_data(file_path):
    info = ''
    params = None
    try:
        with Image.open(file_path) as img:
            info = read_sd_webui_gen_info_from_image(img, file_path)
            params = parse_generation_parameters(info)
    except Exception as e:
        if is_dev:
            print("get_exif_data error %s", e)
    return params, info


def update_image_data(search_dirs: List[str], is_rebuild = False):
    conn = DataBase.get_conn()
    tag_incr_count_rec: Dict[int, int] = {}

    def safe_save_img_tag(img_tag: ImageTag):
        tag_incr_count_rec[img_tag.tag_id] = (
            tag_incr_count_rec.get(img_tag.tag_id, 0) + 1
        )
        # img_tag.save_or_ignore(conn)  # Originally used to deal with some accidents, but the writing was completely fine at all, and the Try Catch was removed

    # Recursively processing each folder
    def process_folder(folder_path: str):
        # check if folder_path exists
        if not os.path.exists(folder_path):
            return
        if not is_rebuild and not Folder.check_need_update(conn, folder_path):
            return
        print(f"Processing folder: {folder_path}")
        for filename in os.listdir(folder_path):
            file_path = os.path.normpath(os.path.join(folder_path, filename))

            if os.path.isdir(file_path):
                process_folder(file_path)

            elif is_valid_image_path(file_path):
                img = DbImg.get(conn, file_path)
                if img:  # Existing skipping
                    continue
                parsed_params, info = get_exif_data(file_path)
                if parsed_params is None or info is None:
                    continue
                img = DbImg(
                    file_path,
                    info,
                    parsed_params["pos_all"],
                    os.path.getsize(file_path),
                    get_modified_date(file_path),
                )
                img.save(conn)

                if not parsed_params:
                    continue
                meta = parsed_params.get("meta", {})
                lora = parsed_params.get("lora", [])
                lyco = parsed_params.get("lyco", [])
                pos = parsed_params["pos_prompt"]
                size_tag = Tag.get_or_create(
                    conn,
                    str(meta.get("Size-1", 0)) + " * " + str(meta.get("Size-2", 0)),
                    type="size",
                )

                for k in [
                    "Model",
                    "Sampler",
                    "Postprocess upscale by",
                    "Postprocess upscaler",
                ]:
                    v = meta.get(k)
                    if not v:
                        continue
                    tag = Tag.get_or_create(conn, str(v), k)
                    safe_save_img_tag(ImageTag(img.id, tag.id))
                for i in lora:
                    tag = Tag.get_or_create(conn, i["name"], "lora")
                    safe_save_img_tag(ImageTag(img.id, tag.id))
                for i in lyco:
                    tag = Tag.get_or_create(conn, i["name"], "lyco")
                    safe_save_img_tag(ImageTag(img.id, tag.id))
                for k in pos:
                    tag = Tag.get_or_create(conn, k, "pos")
                    safe_save_img_tag(ImageTag(img.id, tag.id))
                # NEG temporarily skipped and I feel that no one will search for this

        # Submit to the database change
        Folder.update_modified_date_or_create(conn, folder_path)
        conn.commit()

    for dir in search_dirs:
        process_folder(dir)
        conn.commit()
    for tag_id in tag_incr_count_rec:
        tag = Tag.get(conn, tag_id)
        tag.count += tag_incr_count_rec[tag_id]
        tag.save(conn)
    conn.commit()
    conn.close()
    DataBase.reConnect = True

def rebuild_image_index(search_dirs: List[str]):
    conn = DataBase.get_conn()
    with closing(conn.cursor()) as cur:
        cur.execute(
            """DELETE FROM image_tag
            WHERE image_tag.tag_id IN (
                SELECT tag.id FROM tag WHERE tag.type <> 'custom'
            )
            """
        )
        cur.execute("""DELETE FROM tag WHERE tag.type <> 'custom'""")
        conn.commit()
        update_image_data(search_dirs=search_dirs, is_rebuild=True)