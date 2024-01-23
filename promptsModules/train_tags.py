# -*- coding:utf-8 -*-

import os
import re
from collections import Counter
import json

def handle_train_tag(folder_path, alias_name:str):
    folder_path = os.path.normpath(folder_path)
    # 检查文件夹路径是否存在
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print(f"文件夹路径 '{folder_path}' 不存在或不是文件夹。")
        return
    # 存储所有标签的计数
    tag_counter = Counter()

    # 提取文件夹的文件名并打印
    folder_name = os.path.basename(folder_path)
    print(f"文件夹名: {folder_name}")
    if alias_name is None or alias_name == "":
        alias_name = folder_name

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # 检查文件是否以 ".txt" 结尾
        if filename.endswith(".txt") and os.path.isfile(filepath):
            # 读取文件中的文本
            with open(filepath, 'r', encoding='utf-8') as file:
                file_content = file.read()

                # 使用正则表达式提取文本中的标签
                tags = re.findall(r'\b([^\s,]+)\b', file_content)

                # 更新标签计数
                tag_counter.update(tags)
    json_str = json.dumps(tag_counter, ensure_ascii=False)
    print(json_str)
    return json_str, alias_name


