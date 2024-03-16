# -*- coding:utf-8 -*-
import json
import sqlite3
from enum import IntEnum


def convert_enum_to_int(data):
    # The key value pair in the dictionary
    for key, value in data.items():
        # Check whether the value is intenum type
        if isinstance(value, IntEnum):
            # Convert the Intenum value to an integer
            data[key] = value.value

    return data


def dict_to_string(data):
    # Convert the dictionary data to JSON string
    json_string = json.dumps(data)
    return json_string


def string_to_dict(json_string):
    # Convert json string to dictionary data
    data = json.loads(json_string)
    return data


def store_data_in_database(data, alias_name):
    # Convert data to string
    convert_data = convert_enum_to_int(data)
    json_string = dict_to_string(convert_data)

    # Storage string to database
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
        print("{}The configuration already exists, do you want to update the configuration?".format(alias_name))
        user_input = input("please enter 'yes/y/Y' Confirm the update configuration:")

        if user_input.lower() == 'yes' or user_input.lower() == 'y':
            # Update the existing configuration
            cursor.execute("UPDATE t_config SET config = ?, update_time = datetime('now') WHERE alias = ?",
                           (json_string, alias_name,))
            conn.commit()
            conn.close()
            print("{}The configuration has been updated.".format(alias_name))
        else:
            conn.close()
            print("Cancel the update configuration.")
            return
    else:
        cursor.execute("INSERT INTO t_config (config, alias, update_time) VALUES (?, ?, datetime('now'))",
                       (json_string, alias_name,))
        conn.commit()
        conn.close()
        print("Configuration has been stored.")


def retrieve_data_from_database(query_key):
    # Check data from the database
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
        # Convert the string to dictionary data
        data = string_to_dict(json_string)
        return data
    else:
        return None


def list_alias(limit=100):
    # Check data from the database
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
        print("The configuration has been deleted.")
    else:
        print("Can only delete configuration according to ID.")
