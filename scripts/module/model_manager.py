import os

import openpyxl as pyxl


class ModelInfo:
    def __init__(self, id_model, type_model, name_model, trigger_words="", min_widget=0.4, max_widget=1,
                 default_widget=0.6, is_special=False):
        self.id_model = id_model
        self.type_model = type_model
        self.name_model = name_model
        self.trigger_words = trigger_words
        self.min_widget = min_widget
        self.max_widget = max_widget
        self.default_widget = default_widget
        self.is_special = is_special

    def __str__(self):
        return f"{self.id_model} {self.type_model} {self.name_model} {self.trigger_words} {self.min_widget} {self.max_widget} {self.default_widget} {self.is_special}"


def singleton_with_init(cls):
    instances = {}  # 用于存储实例的字典

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
            instances[cls].loadData()
        return instances[cls]

    return get_instance


@singleton_with_init
class LoraConfigManager:
    _data = {}

    def __init__(self):
        pass

    def loadData(self):
        # 获取当前Python文件的路径
        current_file_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_file_path)
        parent_folder = os.path.dirname(current_folder)

        target_file_name = "modelsConfig.xlsx"
        target_file_path = os.path.join(parent_folder, target_file_name)

        # 检查文件是否存在
        if os.path.exists(target_file_path):
            print(f"find target excel file：{target_file_path}")
            workbook = pyxl.load_workbook(target_file_path)
            sheet = workbook.active
            for row in sheet.iter_rows(min_row=2, values_only=True):  # 从第2行开始遍历
                id_model = row[0]
                type_model = row[1]
                name_model = row[2]
                trigger_words = row[3]
                min_widget = row[4]
                max_widget = row[5]
                default_widget = row[6]
                is_special = row[7]

                if id_model is None or type_model is None or name_model is None:
                    continue

                if trigger_words is not None and isinstance(trigger_words, str) and trigger_words.endswith(","):
                    trigger_words = trigger_words[:-1]
                else:
                    trigger_words = ""

                if min_widget is not None:
                    if isinstance(min_widget, str) and min_widget.isdigit():
                        min_widget = float(min_widget)
                else:
                    min_widget = 0.4
                if max_widget is not None:
                    if isinstance(max_widget, str) and max_widget.isdigit():
                        max_widget = float(max_widget)
                    else:
                        max_widget = 1
                else:
                    max_widget = 1
                if default_widget is not None:
                    if isinstance(default_widget, str) and default_widget.isdigit():
                        default_widget = float(default_widget)
                    else:
                        default_widget = 0.6
                else:
                    default_widget = 0.6

                is_special = (is_special == 1)
                model_obj = ModelInfo(id_model, type_model, name_model, trigger_words, min_widget, max_widget,
                                      default_widget, is_special)
                print(model_obj)
                identifer = f"{id_model}_{type_model}"
                self._data[identifer] = model_obj

        else:
            print(f"can NOT find target excel file：{target_file_path}")

    def query_data(self, model_id):
        return self._data[model_id]
