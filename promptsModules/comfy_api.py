# -*- coding:utf-8 -*-

import hashlib
import os
import random
import time
from urllib import request
import asyncio

import requests

COMFYUI_API_URL = "http://127.0.0.1:8188"


def generate_large_seed():
    """
    Generate a truly random large seed number.

    Uses multiple sources of randomness to ensure uniqueness:
    - Current timestamp
    - Process ID
    - Random bytes from os.urandom()
    - A random float

    Returns:
        int: A large random seed number
    """
    # 获取当前时间戳的微秒部分
    timestamp = time.time_ns()

    # 获取进程ID
    pid = os.getpid()

    # 生成一些随机字节
    random_bytes = os.urandom(16)

    # 生成一个随机浮点数
    random_float = random.random()

    # 组合这些源以创建一个独特的种子字符串
    seed_string = f"{timestamp}_{pid}_{random_bytes}_{random_float}"

    # 使用哈希函数创建一个大的随机数
    hash_object = hashlib.sha256(seed_string.encode())

    # 将哈希转换为大整数
    large_seed = int(hash_object.hexdigest(), 16)

    # 截取一个15位数的大种子
    return int(str(large_seed)[:15])


def load_comfy_ui_loras(lora_path):
    """
    加载指定目录下所有.safetensors文件路径。

    Args:
        lora_path (str): 文件夹路径。

    Returns:
        list: 文件路径列表。
    """
    safetensors_files = []
    try:
        # 判断路径是否存在
        if not os.path.exists(lora_path):
            return safetensors_files

        # 遍历根目录和子目录
        for root, dirs, files in os.walk(lora_path):
            # 遍历文件
            for file in files:
                # 判断文件后缀是否为.safetensors
                if file.endswith(".safetensors"):
                    # 构造相对路径
                    relative_path = os.path.relpath(root, lora_path)
                    if relative_path == '.':
                        # 根目录下的文件，直接添加文件名
                        safetensors_files.append(file)
                    else:
                        # 子目录下的文件，添加相对路径和文件名
                        safetensors_files.append(os.path.join(relative_path, file))
    except Exception as e:
        print(f"发生异常：{e}")
    return safetensors_files


import json


def load_comfyui_workflow(workflow_path):
    """
    加载指定workflow json文件中的内容。

    Args:
        workflow_path (str): json文件路径。

    Returns:
        dict: json文件中的内容。
    """
    try:
        with open(workflow_path, 'r', encoding='utf-8') as file:
            json_flow = file.read()
            return json.loads(json_flow)
    except FileNotFoundError:
        print(f"文件{workflow_path}不存在")
        return None
    except json.JSONDecodeError:
        print(f"文件{workflow_path}不是有效的json文件")
        return None
    except Exception as e:
        print(f"发生异常：{e}")
        return None


def queue_count():
    try:
        # 构造URL
        url = f"{COMFYUI_API_URL}/prompt"
        req = request.Request(url, method='GET')
        with request.urlopen(req) as response:
            # Read and decode the response
            response_data = response.read().decode('utf-8')
            # 解析JSON数据
            json_data = json.loads(response_data)
            # 返回queue_remaining的值
            return json_data['exec_info']['queue_remaining']
    except ConnectionRefusedError:
        print("连接被拒绝，可能是API服务未启动")
        return None
    except Exception as e:
        print(f"发生异常：{e}")
        return None


def clear_queue():
    url = f'{COMFYUI_API_URL}/api/queue'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Content-Type': 'application/json'
    }
    data = {
        'clear': True
    }

    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    if response.status_code == 200:
        return 'success'


def queue_prompt(prompt):
    """
    将prompt发送到指定API并获取响应。

    Args:
        prompt (str): 要发送的prompt。

    Returns:
        str: API响应内容。
    """
    try:
        p = {"prompt": prompt}
        data = json.dumps(p).encode('utf-8')
        req = request.Request(f"{COMFYUI_API_URL}/prompt", data=data)
        with request.urlopen(req) as response:
            # Read and decode the response
            response_data = response.read().decode('utf-8')
            print(f"API Response: {response_data}")
            return response_data
    except ConnectionRefusedError:
        return "连接被拒绝，可能是API服务未启动"
    except Exception as e:
        return f"{e}"


async def start_run_comfyui_workflow(origin_workflow, prompt, gen_num, lora_first, lora_first_strength, enable_second,
                               lora_second, lora_second_strength, lora_second_clip_strength, img_size):
    # copy workflow to avoid changing the original one
    workflow = origin_workflow.copy()
    workflow["76"]["inputs"]["string"] = prompt

    # config lora
    # first lora
    workflow["89"]["inputs"]["lora_name"] = lora_first
    workflow["90"]["inputs"]["float"] = lora_first_strength  # strength_model
    # second lora
    workflow["104"]["inputs"]["switch"] = "On" if enable_second else "Off"
    if not enable_second:
        workflow["104"]["inputs"]["lora_name"] = 'None'
    else:
        workflow["104"]["inputs"]["lora_name"] = lora_second
    workflow["104"]["inputs"]["strength_clip"] = lora_second_clip_strength
    workflow["116"]["inputs"]["float"] = lora_second_strength  # strength_model
    workflow["119"]["inputs"]["boolean"] = enable_second

    # image size
    workflow["102"]["inputs"]["resolution"] = img_size

    result = []

    for i in range(gen_num):

        # 生成并设置随机种子
        random_seed = generate_large_seed()
        print(f"Execution {i + 1} - Generated Seed: {random_seed}")
        workflow["86"]["inputs"]["seed"] = random_seed

        # 调用 API
        success = queue_prompt(workflow)
        result.append(success)

        if i < gen_num - 1:
            await asyncio.sleep(1)
            print(f"Continuing to next execution...")

    return result
