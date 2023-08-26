# -*- coding:utf-8 -*-

import os
import random
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from model_manager import (ModelInfo, LoraConfigManager)

global_random_f = False


def get_single_lora_prompt(category, weight=None):
    prompt = ""
    lora = LoraConfigManager()
    model = lora.query_data(f"{category}_1")
    if isinstance(model, ModelInfo):

        if model.trigger_words != "":
            prompt = "{},<lora:{}:{}>,".format(model.trigger_words, model.name_model,
                                               get_random_weight(model.min_widget, model.max_widget,
                                                                 model.default_widget, weight))

        else:
            prompt = "<lora:{}:{}>,".format(model.name_model,
                                            get_random_weight(model.min_widget, model.max_widget, model.default_widget,
                                                              weight))

    return prompt


def get_single_lycoris_prompt(category, weight=None):
    prompt = ""
    model = LoraConfigManager().query_data(f"{category}_2")
    if isinstance(model, ModelInfo):

        if model.trigger_words != "":
            prompt = "{},<lyco:{}:{}>,".format(model.trigger_words, model.name_model,
                                               get_random_weight(model.min_widget, model.max_widget,
                                                                 model.default_widget, weight))

        else:
            prompt = "<lyco:{}:{}>,".format(model.name_model,
                                            get_random_weight(model.min_widget, model.max_widget, model.default_widget,
                                                              weight))
    return prompt


def get_random_weight(from_v, to_v=1.0, default_v=0.6, weight=None):
    if weight is not None and isinstance(weight, str):
        return weight
    final_v = 0
    if global_random_f is not True:
        final_v = default_v
    else:
        final_v = random.uniform(from_v, to_v)
    return "{:.2f}".format(final_v)


def gen_lora_prompt_list(lora_list, random_f=False):
    global global_random_f
    global_random_f = random_f
    prompt_list = []
    for lora in lora_list:
        lora_name, weight, prompt_type = convert_widget_string(lora)
        prompt_list.append(get_single_lora_prompt(lora_name, weight))
    prompt = "".join(prompt_list)
    return prompt


def gen_lycoris_prompt_list(lycoris_list, random_f=False):
    global global_random_f
    global_random_f = random_f
    prompt_list = []
    for lyco in lycoris_list:
        lyco_name, weight, prompt_type = convert_widget_string(lyco)
        prompt_list.append(get_single_lycoris_prompt(lyco_name, weight))
    prompt = "".join(prompt_list)
    return prompt


def get_embed_prompt(embedding_list):
    global global_random_f
    global_random_f = True
    prompt_list = []
    for embedding_str in embedding_list:
        embedding, weight, prompt_type = convert_widget_string(embedding_str)
        prompt_list.append(get_single_embedding_prompt(embedding, weight))

    prompt = "".join(prompt_list)
    return prompt


def get_single_embedding_prompt(category, weight=None):
    prompt = ""
    model = LoraConfigManager().query_data(f"{category}_3")
    if isinstance(model, ModelInfo):

        if model.trigger_words != "":
            prompt = "({}:{}), {},".format(model.name_model,
                                           get_random_weight(model.min_widget, model.max_widget, model.default_widget,
                                                             weight), model.trigger_words)

        else:
            prompt = "({}:{}),".format(model.name_model,
                                       get_random_weight(model.min_widget, model.max_widget, model.default_widget,
                                                         weight))
    return prompt


def convert_widget_string(model_str):
    # check if model_str is int or float
    if isinstance(model_str, int) or isinstance(model_str, float):
        return model_str, None, 0
    elif isinstance(model_str, str):

        if ':' in model_str:
            splitted = model_str.split(':')
            before_colon = int(splitted[0])
            after_colon = splitted[1]
            prompt_type = '0'
            if len(splitted) > 2:
                prompt_type = splitted[2]
            if prompt_type is not None and prompt_type.isdigit():
                prompt_type = int(prompt_type)
            return before_colon, after_colon, prompt_type
        else:
            result = None
            if model_str.isdigit():
                result = int(model_str)
            return result, None, 0
    else:
        raise ValueError("model_str is not int or float or str")


def should_re_gen_prompt(lora_list):
    if len(lora_list) <= 0:
        return False
    return True


def is_special_single(lora_list):
    return False
