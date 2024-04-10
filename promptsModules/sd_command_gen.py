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
<lora:cutegirl25d:0.4>, 1girl, (smile), cute, 18yo,
lishi,1girl,solo,lips, makeup,  looking at viewer,  smile, side blunt bangs,  ultra detailed, 8k,   <lora:face_lishi_v1-000007:0.5>
"""

project_config = {
    # "preset": 2,
    "lora": [101],  # x
    "lyco": [],  # y
    "embeddings": [],  # z
    "models_order": 'xyz',  # lora, lyco, embeddings Output order xyz
    "lora_weights_random": True,
    "additional_prompt": "",

    # Perspective
    "angle": "null",  # null is disabled
    "body_framing": "null",
    "dynamic_mode": False,
    "pose_type": 1,  # base = 1 whole = 2

    # Color, just give color
    "leg_wear_color": "",
    "shoes_color": "",
    "hair_color": "null",
    "enable_eye_color": True,
    "disable_all_color": True,

    # Body wearing
    "breasts_size": "large",  # null is disabled
    # DRESS = 1 UNIFORM = 2 BODYSUIT = 3 TRADITIONAL = 4 CUSTOM = 5 RANDOM = 6 ASNULL = 7
    "body_wear": 7,
    # "top_wear": TopWearType.SHIRTS,
    # "bottom_wear": BottomWearType.SKIRT,
    # socks = 1; knee_highs = 2; over_knee_highs = 3; thigh_highs = 4; pantyhose = 5; bare = 6; as_null = 7; random = 8
    "leg_wear": 7,
    "panties": False,
    # BOOTS, HIGHHEELS, SANDALS, SLIPPERS, BARE, ASNULL = 1, 2, 3, 4, 5, 6
    "shoes_type": 6,

# Directly specify Prompt, which will skip other configurations directly, and automatically deepen the weight of Prompt "assign_focus_on": "null",  # null is disabled
    "assign_pose": "null",  # null is disabled
    "assign_profession": "null",
    "assign_expression": "",
    "assign_shoes": "",
    "assign_leg_wear": "",
    "assign_body_clothes": "",
    "assign_panties": "",
    "assign_girl_description": "",
    "place": "null",

    # Body -related
    "body_with": False,
    "body_status": False,
    "body_description": False,
    "cloth_trim": False,
    "add_focus": False,

    "nsfw_type": 3,  # 1 nude 2 sexual 3 normal

    "accessories_random_tims": 1,  # max:6 NOTE：For some models, how to appear these prOMPTs may affect the perspective effect
    "suffix_words_random_times": 0,  # Sabbage dotted random number
    "object_random_times": 1,  # max: 6
    "sexual_list_random_index_times": 1,  # max:5
    "nude_list_random_index_times": 0,  # max:9
    "is_simple_nude": True,

    # Character description
    "has_girl_desc": False,  # Whether to add ultra -long girl descriptions, it seems that most of them do not need
    "add_girl_beautyful": False,  # Girl prefix description
    "add_hair_style": False,  # Whether to add hairstyle description

    # Other configuration
    "is_realistic": True,
    "use_starting": True,  # Do you use a spell to start?
    "add_colors": False,
    "enable_day_weather": False,  # Whether to enable the weather
    "enable_light_effect": True,  # Light effect
    "enable_image_tech": False,  # Image technology

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
    # The key value pair in the dictionary
    for key, value in data.items():
        # Check whether the value is intenum type
        if isinstance(value, IntEnum):
            # Convert the Intenum value to an integer
            data[key] = value.value

    return data


def main():
    # Create a parameter parser
    parser = argparse.ArgumentParser()

    # Add command line parameters
    parser.add_argument("--m", default='1', help="""
    Run mode:
    m = 1 means a simple mode, only prompt, and the configuration is not saved
    m = 2 means generating prompt and saving the configuration 
    m = 3 read the configuration according to alias, and use this configuration to generate Prompt 
    m = 4 List the saved alias 
    m = 5 Delete saved alias, delete it according to ID
    """)
    parser.add_argument("--s", default='', required=False, help="""
    Save the configuration Alias, only effective at m = 2/3    """)
    parser.add_argument("--n", default='4', required=False, help="Generate the quantity of Prompt, default")
    parser.add_argument("--ls", default='100', required=False, help="Query alias quantity, default")

    # Analyze command line parameters
    args = parser.parse_args()

    # Get parameter value
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
            print("Alias or ID that is not found in this configuration, please check whether the input is correct")
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
            # Change the line to print the next line
            print()
    elif arg_mode == '5':
        delete_data_from_database(arg_alias)
    else:
        create_prompts(int(arg_gen_number))


if __name__ == '__main__':
    main()
