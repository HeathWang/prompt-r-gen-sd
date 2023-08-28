# -*- coding:utf-8 -*-

import random

from promptsModules.model_manager import (ModelInfo, LoraConfigManager)

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
        lora_name, weight = convert_widget_string(lora)
        prompt_list.append(get_single_lora_prompt(lora_name, weight))
    prompt = "".join(prompt_list)
    return prompt


def gen_lycoris_prompt_list(lycoris_list, random_f=False):
    global global_random_f
    global_random_f = random_f
    prompt_list = []
    for lyco in lycoris_list:
        lyco_name, weight = convert_widget_string(lyco)
        prompt_list.append(get_single_lycoris_prompt(lyco_name, weight))
    prompt = "".join(prompt_list)
    return prompt


def get_embed_prompt(embedding_list):
    global global_random_f
    global_random_f = True
    prompt_list = []
    for embedding_str in embedding_list:
        embedding, weight = convert_widget_string(embedding_str)
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
        return model_str, None
    elif isinstance(model_str, str):

        if ':' in model_str:
            splitted = model_str.split(':')
            before_colon = splitted[0]
            after_colon = splitted[1]
            return before_colon, after_colon
        else:
            return model_str, None
    else:
        raise ValueError("CAN NOT VALIDATE MODEL STRING")


def should_re_gen_prompt(lora_list):
    if len(lora_list) <= 0:
        return False
    return True


def is_special_single(model_list):
    for model in model_list:
        model_name, weight = convert_widget_string(model)
        if LoraConfigManager().check_special(model_name):
            return True
    return False
