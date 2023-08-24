# -*- coding:utf-8 -*-

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

from module.promptGen import gen_prompt


def create_prompts(prompt_count, project_config):
    prompts = ""

    for i in range(prompt_count):
        prompt_tmp, config = gen_prompt(project_config)
        prompts = prompts + prompt_tmp + "\n"
    return prompts
