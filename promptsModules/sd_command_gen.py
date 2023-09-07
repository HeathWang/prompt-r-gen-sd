# -*- coding:utf-8 -*-

import argparse
from enum import IntEnum

from promptsModules.configDB import (store_data_in_database, retrieve_data_from_database, list_alias,
                             delete_data_from_database)
from promptsModules.promptGen import (gen_prompt)

output_file_name = "prompts.txt"

"""
// lora
CHARACTER_ST_LOUIS = 201, POSE_SIT_CROSSLEG = 626, FUNC_DETAIL_TWEAKER = 901, FUNC_AHEGAO = 903, FUNC_ADD_CUMBERSOME = 904,
BODY_PERFECT_FULL_ROUND_BREASTS_SLIM_WAIST = 503,
// lyco
BACKGROUND_HALATION = 402, STYLE_BEAUTYLEGS = 601, STYLE_ABSTRACT_DREAMWAVE = 202
"""

"""
// adetailer prompt:
<lora:MengX girl_Mix:0.8>, 1girl, smile, cute, 18yo, extremely detailed eyes and face, beautiful face,
<lora:cutegirl25d:0.4>, 1girl, (smile), cute, 18yo, extremely detailed eyes and face, beautiful face,
"""

project_config = {
    # "preset": 2,
    "lora": [101],  # x
    "lyco": [],  # y
    "embeddings": [],  # z
    "models_order": 'xyz',  # lora, lyco, embeddings 输出顺序xyz
    "lora_weights_random": True,
    "additional_prompt": "",

    # 视角动作
    "angle": "null",  # null则禁用
    "body_framing": "null",
    "dynamic_mode": False,
    "pose_type": 1,  # base = 1 whole = 2

    # 颜色，只用给颜色即可
    "leg_wear_color": "",
    "shoes_color": "",
    "hair_color": "null",
    "enable_eye_color": True,
    "disable_all_color": True,

    # 身体穿着
    "breasts_size": "large",  # null则禁用
    # DRESS = 1 UNIFORM = 2 BODYSUIT = 3 TRADITIONAL = 4 CUSTOM = 5 RANDOM = 6 ASNULL = 7
    "body_wear": 7,
    # "top_wear": TopWearType.SHIRTS,
    # "bottom_wear": BottomWearType.SKIRT,
    # socks = 1; knee_highs = 2; over_knee_highs = 3; thigh_highs = 4; pantyhose = 5; bare = 6; as_null = 7; random = 8
    "leg_wear": 7,
    "panties": False,
    # BOOTS, HIGHHEELS, SANDALS, SLIPPERS, BARE, ASNULL = 1, 2, 3, 4, 5, 6
    "shoes_type": 6,

    # 直接指定prompt，这会直接跳过其他配置，并且自动加深prompt权重
    "assign_focus_on": "null",  # null则禁用
    "assign_pose": "null",  # null则禁用
    "assign_profession": "null",
    "assign_expression": "",
    "assign_shoes": "",
    "assign_leg_wear": "",
    "assign_body_clothes": "",
    "assign_panties": "",
    "assign_girl_description": "",
    "place": "null",

    # 身体相关
    "body_with": False,
    "body_status": False,
    "body_description": False,
    "cloth_trim": False,
    "add_focus": False,

    "nsfw_type": 3,  # 1 nude 2 sexual 3 normal

    "accessories_random_tims": 0,  # max:6 NOTE：对于某些model，如何这些prompt出现，可能会影响视角效果
    "suffix_words_random_times": 0,  # 形容词缀随机次数
    "object_random_times": 0,  # max: 6
    "sexual_list_random_index_times": 0,  # max:5
    "nude_list_random_index_times": 0,  # max:9
    "is_simple_nude": True,

    # 人物描述
    "has_girl_desc": False,  # 是否加入超长的girl描述，目前看来大部分不需要
    "add_girl_beautyful": False,  # girl前缀描述
    "add_hair_style": False,  # 是否加入发型描述

    # 其他配置
    "is_realistic": False,
    "use_starting": True,  # 是否使用咒语起手式
    "add_colors": False,
    "enable_day_weather": False,  # 是否启用天气
    "enable_light_effect": True,  # 灯光效果
    "enable_image_tech": False,  # 图像技术

}


def open_file(file_name):
    return open(file_name, 'w')


def create_prompts(prompt_count):
    prompts = ""
    config_ = {}
    f = open_file(output_file_name)

    for i in range(prompt_count):
        prompt_tmp, config = gen_prompt(project_config)
        prompts = prompts + prompt_tmp + "\n"
        config_ = config

    target = str(config_) + "\n\n\n" + prompts
    f.write(target)
    return config_


def convert_enum_to_int(data):
    # 遍历字典中的键值对
    for key, value in data.items():
        # 检查值是否为IntEnum类型
        if isinstance(value, IntEnum):
            # 将IntEnum值转换为整数
            data[key] = value.value

    return data


def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser()

    # 添加命令行参数
    parser.add_argument("--m", default='1', help="""
    运行模式：
    m = 1 表示简单模式，只生成prompt，不保存该次配置
    m = 2 表示生成prompt，并保存该次配置
    m = 3 根据alias读取配置，并使用该配置生成prompt
    m = 4 列出保存的alias
    m = 5 删除保存的alias，根据id删除
    """)
    parser.add_argument("--s", default='', required=False, help="""
    保存配置的alias，仅在m = 2/3时有效
    """)
    parser.add_argument("--n", default='4', required=False, help="生成prompt数量，默认为6")
    parser.add_argument("--ls", default='100', required=False, help="查询alias数量，默认为100")

    # 解析命令行参数
    args = parser.parse_args()

    # 获取参数值
    arg_mode = args.m
    arg_alias = args.s
    arg_gen_number = args.n
    arg_query_alias_number = args.ls

    if arg_mode == '2':
        config_callback = create_prompts(int(arg_gen_number))
        store_data_in_database(config_callback, arg_alias)
    elif arg_mode == '3':
        query_result = retrieve_data_from_database(arg_alias)
        if query_result is None:
            print("未找到该配置的alias或id，请检查输入是否正确")
        else:
            global project_config
            project_config = query_result
            create_prompts(int(arg_gen_number))
    elif arg_mode == '4':
        results = list_alias(int(arg_query_alias_number))
        for i in range(0, len(results), 2):
            print(results[i], end=" ")
            if i + 1 < len(results):
                print(results[i + 1], end=" ")
            # 换行打印下一行
            print()
    elif arg_mode == '5':
        delete_data_from_database(arg_alias)
    else:
        create_prompts(int(arg_gen_number))


if __name__ == '__main__':
    main()
