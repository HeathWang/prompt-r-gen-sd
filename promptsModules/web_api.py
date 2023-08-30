# -*- coding:utf-8 -*-

from promptsModules.promptGen import gen_prompt
import re


def create_prompts(prompt_count, project_config):
    prompts = ""

    for i in range(prompt_count):
        prompt_tmp, config = gen_prompt(project_config)
        prompts = prompts + prompt_tmp + "\n"
    prompts = re.sub(r'\n+$', '', prompts)
    return prompts
