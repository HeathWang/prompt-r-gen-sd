# -*- coding:utf-8 -*-

from enum import IntEnum

from scripts.module.basePromptBuilder import (
    get_config_value_by_key,
    get_starting_prompt, get_user_additional_prompt, get_realistic_prompt, get_angle_and_image_composition,
    get_girl_desc_prompt, get_job_prompt, get_body_wear_prompt, get_hair_eyes_prompt, get_place_prompt,
    get_bottom_prompt, LegWearType, NSFWType, FaceExpression, FootWearType, get_nsfw_prompt, get_uncensored_prompt,
    SexActType, get_s_act_sex_prompt, get_s_act_group_prompt, get_s_act_tentacles_prompt, BodyWearType, project_config
)
# import basePromptBuilder as pb
from scripts.module.lora import (
    gen_lora_prompt_list, gen_lycoris_prompt_list, get_embed_prompt, is_special_single, gen_lora_special,
    should_re_gen_prompt
)


class DefaultConfig(IntEnum):
    DEFAULT = 1
    WALLPAPER = 2  # 壁纸
    CROSSLEGS = 3
    NUDESIMPLE1 = 4  # nude, 精简模式，较多饰物，无nude其他prompt
    NUDEDEFAULT = 5  # nude, 非精简模式，较多饰物，少量nude prompt
    NUDEDEFAULT_BACK = 6  # nude, 背部
    NORMAL_DRESS = 7
    SEXAULDEFAULT = 8


def get_lora_prompt(lora_list):
    return gen_lora_prompt_list(lora_list, get_config_value_by_key("lora_weights_random"))


def get_lyco_prompt(lyco_list):
    return gen_lycoris_prompt_list(lyco_list, get_config_value_by_key("lora_weights_random"))


def get_embeddings_prompt():
    return get_embed_prompt(get_config_value_by_key("embeddings"))


def gen_lora_prompt():
    lora_list = get_config_value_by_key("lora")
    lyco_list = get_config_value_by_key("lyco")
    order_list = get_config_value_by_key("models_order")
    # order_list为string，按照字符，拆分为数组
    order_arr = [char for char in order_list]
    prompt = ""
    if is_special_single(lora_list) or is_special_single(lyco_list):
        for v in order_arr:
            if v == 'x':
                prompt = prompt + gen_lora_special(lora_list)
            elif v == 'y':
                prompt = prompt + get_lyco_prompt(lyco_list)
            elif v == 'z':
                prompt = prompt + get_embeddings_prompt()
        prompt = prompt \
                 + get_starting_prompt() \
                 + get_user_additional_prompt() \
                 + get_realistic_prompt() \
                 + "\n"

    else:
        for_lora_config = {

            # 颜色，只用给颜色即可
            "disable_all_color": True,

            # 直接指定prompt，这会直接跳过其他配置，并且自动加深prompt权重
            "assign_focus_on": "null",  # null则禁用
            "assign_profession": "null",

            # "body_with": False,
            # "body_status": False,

            "is_simple_nude": True,

            # "accessories_random_tims": 0,  # max:6 NOTE：对于某些model，如何这些prompt出现，可能会影响视角效果
            # "object_random_times": 0,  # max: 6
            # "sexual_list_random_index_times": 0,  # max:5
            # "nude_list_random_index_times": 0,  # max:9

            # 其他配置
            # "is_realistic": True,
            # "use_starting": False,  # 是否使用咒语起手式

        }
        for key in for_lora_config:
            if key in project_config:
                project_config[key] = for_lora_config[key]

        for v in order_arr:
            if v == 'x':
                prompt = prompt + get_lora_prompt(lora_list)
            elif v == 'y':
                prompt = prompt + get_lyco_prompt(lyco_list)
            elif v == 'z':
                prompt = prompt + get_embeddings_prompt()
        prompt = prompt \
                 + get_user_additional_prompt() \
                 + get_realistic_prompt() \
                 + get_angle_and_image_composition() \
                 + get_girl_desc_prompt() \
                 + get_job_prompt() \
                 + get_body_wear_prompt() \
                 + get_hair_eyes_prompt() \
                 + get_place_prompt() \
                 + get_starting_prompt() \
                 + get_bottom_prompt() \
                 + "\n"
    return prompt


def get_preset_config_map(preset_type):
    if preset_type == DefaultConfig.DEFAULT:
        return {}
    elif preset_type == DefaultConfig.WALLPAPER:
        return {
            "angle": "null",
            "body_framing": "portrait",
            "add_focus": False,
            "breasts_size": "null",
            "leg_wear": LegWearType.ASNULL,
            "panties": False,
            "shoes_type": FootWearType.ASNULL,
            "body_with": False,
            "body_status": False,
            "assign_pose": "null",
            "assign_expression": "smile",
            "accessories_random_tims": 0,
            "object_random_times": 3,
            "nsfw_type": NSFWType.NOTNSFW,
            "is_nsfw": False,
            "sex_mode": False,
            "is_realistic": True,
        }
    elif preset_type == DefaultConfig.CROSSLEGS:
        return {
            "angle": "null",
            "body_framing": "lower body",
            "assign_focus_on": "leg focus",
            "breasts_size": "medium",
            "leg_wear": LegWearType.PANTYHOSE,
            "panties": False,
            "body_with": False,
            "body_status": False,
            "assign_pose": "sitting, crossed legs",
            "assign_expression": "smile",
            "assign_shoes": "high heels",
            "accessories_random_tims": 4,
            "object_random_times": 3,
            "nsfw_type": NSFWType.NOTNSFW,
            "is_nsfw": False,
            "sex_mode": False,
            "is_realistic": True,
        }
    elif preset_type == DefaultConfig.NORMAL_DRESS:
        return {
            "body_wear": BodyWearType.DRESS,
            "leg_wear": LegWearType.PANTYHOSE,
            "panties": False,
            "accessories_random_tims": 3,
            "object_random_times": 3,
            "nsfw_type": NSFWType.NOTNSFW,
            "sex_mode": False,
        }
    elif preset_type == DefaultConfig.SEXAULDEFAULT:
        return {
            "panties": True,
            "accessories_random_tims": 3,
            "object_random_times": 2,
            "sexual_list_random_index_times": 3,
            "nsfw_type": NSFWType.SEXUAL,
            "sex_mode": False,
        }
    elif preset_type == DefaultConfig.NUDESIMPLE1 \
            or preset_type == DefaultConfig.NUDEDEFAULT \
            or preset_type == DefaultConfig.NUDEDEFAULT_BACK:
        nude_config = {
            "face_expression": FaceExpression.SEXUAL,
            "breasts_size": "large",
            "leg_wear": LegWearType.RANDON,
            "panties": True,
            "shoes_type": FootWearType.ASNULL,
            "body_with": True,
            "body_status": False,
            "accessories_random_tims": 4,
            "object_random_times": 2,

            "nsfw_type": NSFWType.NUDE,
            "nude_list_random_index_times": 0,  # max:9
            "is_nsfw": False,
            "is_simple_nude": True,
            "nude_strong": False,
        }
        if preset_type == DefaultConfig.NUDESIMPLE1:
            pass
        elif preset_type == DefaultConfig.NUDEDEFAULT:
            nude_config["nude_list_random_index_times"] = 2
            nude_config["is_simple_nude"] = False
        elif preset_type == DefaultConfig.NUDEDEFAULT_BACK:
            nude_config["nude_list_random_index_times"] = 2
            nude_config["is_simple_nude"] = False

            nude_config["angle"] = "view from behind"
            nude_config["assign_pose"] = "all fours, sitting"

        return nude_config


def generate_normal_prompts():
    prompts = ""

    if should_re_gen_prompt(get_config_value_by_key("lora")) or should_re_gen_prompt(
            get_config_value_by_key("lyco")):
        prompts = gen_lora_prompt()
    else:

        prompts = prompts \
                  + get_starting_prompt() \
                  + get_user_additional_prompt() \
                  + get_embeddings_prompt() \
                  + get_realistic_prompt() \
                  + get_nsfw_prompt() \
                  + get_angle_and_image_composition() \
                  + get_girl_desc_prompt() \
                  + get_uncensored_prompt() \
                  + get_job_prompt() \
                  + get_body_wear_prompt() \
                  + get_hair_eyes_prompt() \
                  + get_place_prompt() \
                  + get_bottom_prompt() \
                  + "\n"
    return prompts


def generate_sex_prompts():
    prompts = ""
    sex_type = get_config_value_by_key("sex_type")

    if sex_type == SexActType.SEX:
        prompts = get_s_act_sex_prompt()
        prompts = prompts \
                  + get_embeddings_prompt() \
                  + get_lora_prompt()
    elif sex_type == SexActType.GROUP:
        prompts = get_s_act_group_prompt()
    elif sex_type == SexActType.TENTACLES:
        prompts = get_s_act_tentacles_prompt()
    return prompts


def random_prompts():
    if get_config_value_by_key("sex_mode"):
        return generate_sex_prompts()
    else:
        return generate_normal_prompts()


def gen_prompt(config_map):
    preset_value = 1
    if "preset" in config_map:
        preset_value = config_map["preset"]
    if preset_value < 1:
        preset_value = 1

    if preset_value is not None and preset_value != 1:
        replace_config_by(config_map)
        preset_map = get_preset_config_map(preset_value)
        replace_config_by(preset_map)
    else:
        replace_config_by(config_map)

    return random_prompts(), project_config


def replace_config_by(custom_map):
    # update project_config by replace the key which exists in config_map
    for key in custom_map:
        # check if the key exists in project_config
        if key in project_config:
            project_config[key] = custom_map[key]


def command_ls():
    return command_ls()


def command_send(the_key):
    return command_send(the_key)
