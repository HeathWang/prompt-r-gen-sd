# -*- coding:utf-8 -*-
import json
import sqlite3
from enum import IntEnum


def convert_enum_to_int(data):
    # 遍历字典中的键值对
    for key, value in data.items():
        # 检查值是否为IntEnum类型
        if isinstance(value, IntEnum):
            # 将IntEnum值转换为整数
            data[key] = value.value

    return data


def dict_to_string(data):
    # 将字典数据转换为JSON字符串
    json_string = json.dumps(data)
    return json_string


def string_to_dict(json_string):
    # 将JSON字符串转换为字典数据
    data = json.loads(json_string)
    return data


def store_data_in_database(data, alias_name):
    # 将数据转换为字符串
    convert_data = convert_enum_to_int(data)
    json_string = dict_to_string(convert_data)

    # 存储字符串到数据库
    conn = sqlite3.connect('prompt.db')
    cursor = conn.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS t_config (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        config TEXT NOT NULL,
                        alias TEXT NOT NULL,
                        update_time TEXT
                    )
                ''')

    # query if the alias exists
    cursor.execute("SELECT id FROM t_config WHERE alias = ? LIMIT 1", (alias_name,))
    result = cursor.fetchone()
    if result is not None:
        print("{}配置已存在，是否要更新配置？".format(alias_name))
        user_input = input("请输入 'yes/y/Y' 确认更新配置：")

        if user_input.lower() == 'yes' or user_input.lower() == 'y':
            # 更新现有配置
            cursor.execute("UPDATE t_config SET config = ?, update_time = datetime('now') WHERE alias = ?",
                           (json_string, alias_name,))
            conn.commit()
            conn.close()
            print("{}配置已更新。".format(alias_name))
        else:
            conn.close()
            print("取消更新配置。")
            return
    else:
        cursor.execute("INSERT INTO t_config (config, alias, update_time) VALUES (?, ?, datetime('now'))",
                       (json_string, alias_name,))
        conn.commit()
        conn.close()
        print("配置已存储完成.")


def retrieve_data_from_database(query_key):
    # 从数据库查询数据
    conn = sqlite3.connect('prompt.db')
    cursor = conn.cursor()

    if query_key.isdigit():
        cursor.execute("SELECT config FROM t_config WHERE id = ? LIMIT 1", (query_key,))
    else:
        cursor.execute("SELECT config FROM t_config WHERE alias = ? LIMIT 1", (query_key,))
    result = cursor.fetchone()
    conn.close()

    if result is not None:
        json_string = result[0]
        # 将字符串转换为字典数据
        data = string_to_dict(json_string)
        return data
    else:
        return None


def list_alias(limit=100):
    # 从数据库查询数据
    conn = sqlite3.connect('prompt.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, alias,update_time  FROM t_config ORDER BY update_time DESC LIMIT ?", (limit,))
    result = cursor.fetchall()
    conn.close()

    if result is not None:
        return result
    else:
        return None


def delete_data_from_database(arg_alias):
    # delete data with id
    if arg_alias.isdigit():
        conn = sqlite3.connect('prompt.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM t_config WHERE id = ?", (arg_alias,))
        conn.commit()
        conn.close()
        print("配置已删除.")
    else:
        print("只能根据id删除配置.")
