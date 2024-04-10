# -*- coding:utf-8 -*-

import os
import re
from collections import Counter
import json

def handle_train_tag(folder_path, alias_name:str):
    folder_path = os.path.normpath(folder_path)
    file_text_lsit = []

    # Check whether the path path of the folder exists
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print(f"Folder path '{folder_path}' No or not a folder.")
        return
    # Store all tag counts
    tag_counter = Counter()

    # Extract the file name of the folder and print
    folder_name = os.path.basename(folder_path)
    print(f"Folder name: {folder_name}")
    if alias_name is None or alias_name == "":
        alias_name = folder_name

    # All files in the folder
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

    if filename.endswith(".txt") and os.path.isfile(filepath):
        # Read text from file
        with open(filepath, 'r', encoding='utf-8') as file:
            file_content = file.read()
            file_text_lsit.append(file_content)

    # Use the regular expression to extract the label in the text
    tags = re.findall(r'\b([^\s,]+)\b', file_content)

    # Update tag count
    tag_counter.update(tags)
    json_str = json.dumps(tag_counter, ensure_ascii=False)
    print(json_str)
    return json_str, alias_name, file_text_lsit


