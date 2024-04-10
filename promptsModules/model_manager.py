# -*- coding:utf-8 -*-
import os

import openpyxl as pyxl


class ModelInfo:
    def __init__(self, id_model, type_model, name_model, trigger_words="", min_widget=0.4, max_widget=1,
                 default_widget=0.6, is_special=False, user_desc="", sheet_index=1):
        self.id_model = id_model
        self.type_model = type_model
        self.name_model = name_model
        self.trigger_words = trigger_words
        self.min_widget = min_widget
        self.max_widget = max_widget
        self.default_widget = default_widget
        self.is_special = is_special
        self.user_desc = user_desc
        self.sheet_index = sheet_index

    def __str__(self):
        return f"{self.id_model} {self.type_model} {self.name_model} {self.trigger_words} {self.min_widget} {self.max_widget} {self.default_widget} {self.is_special}"


class LoraConfigManager(object):
    _data = {}
    _special_ids = set()
    _lastModifyTime = 0

    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
            cls._instance.loadData()
        return cls._instance

    def __init__(self):
        pass

    def get_excel_file_path(self):
        current_file_path = os.path.abspath(__file__)
        current_folder = os.path.dirname(current_file_path)

        target_file_name = "modelsConfig.xlsx"
        target_file_path = os.path.join(current_folder, target_file_name)
        return target_file_path

    def loadData(self):
        target_file_path = self.get_excel_file_path()

        # Check whether the file exists
        if os.path.exists(target_file_path):
            print(f"loading prompt-r-gen-sd excel file：{target_file_path}")
            self._lastModifyTime = os.path.getmtime(target_file_path)
            workbook = pyxl.load_workbook(target_file_path)
            sheet = workbook.active
            real_index = 0
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Starting from line 2
                id_model = row[0]
                type_model = row[1]
                name_model = row[2]
                trigger_words = row[3]
                min_widget = row[4]
                max_widget = row[5]
                default_widget = row[6]
                is_special = row[7]
                user_desc = row[8]

                if id_model is None or type_model is None or name_model is None:
                    continue

                if trigger_words is not None and isinstance(trigger_words, str) and trigger_words.endswith(","):
                    trigger_words = trigger_words[:-1]
                elif isinstance(trigger_words, str):
                    pass
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
                if default_widget is not None:
                    if isinstance(default_widget, str) and default_widget.isdigit():
                        default_widget = float(default_widget)
                    else:
                        default_widget = 0.6
                else:
                    default_widget = 0.6

                is_special = (is_special == 1)
                real_index += 1
                model_obj = ModelInfo(id_model, type_model, name_model, trigger_words, min_widget, max_widget,
                                      default_widget, is_special, user_desc, real_index)
                # print(model_obj)
                identifer = f"{id_model}_{type_model}"
                if is_special:
                    self._special_ids.add(identifer)
                self._data[identifer] = model_obj
            workbook.close()
        else:
            print(f"can NOT find prompt-r-gen-sd excel file：{target_file_path}")

    def query_data(self, model_id):
        if self._lastModifyTime != os.path.getmtime(self.get_excel_file_path()):
            print("prompt config changed, reloading....")
            self.reload()
            if model_id in self._data:
                return self._data[model_id]
        else:
            if model_id in self._data:
                return self._data[model_id]
        return None

    def reload(self):
        self._lastModifyTime = os.path.getmtime(self.get_excel_file_path())
        self._data = {}
        self._special_ids = set()
        self.loadData()

    def check_special(self, model_id):
        if f"{model_id}_1" in self._special_ids:
            return True
        if f"{model_id}_2" in self._special_ids:
            return True

        return False

    def export_to_data_frame(self):
        data = []
        for key, value in self._data.items():
            obj_index = key.split("_")[0]
            obj_type = value.type_model
            if obj_type == 1 or obj_type == "1":
                obj_type = "Lora"
            elif obj_type == 2 or obj_type == "2":
                obj_type = "Loha"
            elif obj_type == 3 or obj_type == "3":
                obj_type = "Embedding"
            obj_name = value.name_model
            obj_desc = value.user_desc
            sheet_index = value.sheet_index
            data.append([key, sheet_index, obj_index, obj_type, obj_name, obj_desc])

        # sort data with key obj
        data.sort(key=lambda x: x[0])
        # loop data, and remove every firt obj from child node
        for i in range(len(data)):
            data[i].remove(data[i][0])
        return data
