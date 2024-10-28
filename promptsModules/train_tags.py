# -*- coding:utf-8 -*-

import os
import re
from collections import Counter
import json


def handle_train_tag(folder_path, alias_name: str):
    """
    处理训练标签文件夹，返回标签统计和文件内容信息

    Args:
        folder_path: 文件夹路径
        alias_name: 别名

    Returns:
        dict: 包含以下键值:
            - tag_stats: 标签统计信息
            - alias_name: 文件夹别名
            - files: 文件详细信息列表，每个文件包含名称和内容
            - success: 是否成功处理
            - message: 处理结果信息
    """
    folder_path = os.path.normpath(folder_path)
    result = {
        "tag_stats": {},
        "alias_name": "",
        "files": [],
        "success": False,
        "message": ""
    }

    # 检查文件夹路径是否存在
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        result["message"] = f"文件夹路径 '{folder_path}' 不存在或不是文件夹。"
        return result

    # 存储所有标签的计数
    tag_counter = Counter()

    # 提取文件夹的文件名并设置别名
    folder_name = os.path.basename(folder_path)
    if alias_name is None or alias_name == "":
        alias_name = folder_name
    result["alias_name"] = alias_name

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # 检查文件是否以 ".txt" 结尾
        if filename.endswith(".txt") and os.path.isfile(filepath):
            try:
                # 读取文件中的文本
                with open(filepath, 'r', encoding='utf-8') as file:
                    file_content = file.read()

                    # 使用正则表达式提取文本中的标签
                    tags = re.findall(r'\s*([^,]+?)\s*(?=,|$)', file_content)

                    # 更新标签计数
                    tag_counter.update(tags)

                    # 添加文件信息
                    file_info = {
                        "filename": filename,
                        "content": file_content,
                        "tags": tags
                    }
                    result["files"].append(file_info)

            except Exception as e:
                result["message"] += f"\n处理文件 {filename} 时发生错误: {str(e)}"

    # 将Counter对象转换为字典
    result["tag_stats"] = dict(tag_counter)
    result["success"] = True
    result["message"] = "处理完成"

    return result


