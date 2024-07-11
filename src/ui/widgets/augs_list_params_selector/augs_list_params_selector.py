from typing import List
from supervisely.app.widgets import Widget
from supervisely.app import StateJson, DataJson


class AugsListParamsSelector(Widget):
    def __init__(self, config: dict, widget_id: str = None):
        """
        Config example:

        {
            "arithmetic": {
                "Add": {
                    "durl": "https://imgaug.readthedocs.io/en/latest/source/api_augmenters_arithmetic.html#imgaug.augmenters.arithmetic.Add",
                    "py": "iaa.Add(value=(-20, 20), per_channel=False)",
                    "params": [
                        {
                            "type": "el-slider-range",
                            "default": [
                                -20,
                                20
                            ],
                            "min": -255,
                            "max": 255,
                            "pname": "value",
                            "valueType": "int"
                        },
                        {
                            "type": "el-checkbox",
                            "default": false,
                            "pname": "per_channel"
                        }
                    ]
            },
            ...
        }
        """
        if len(config.keys()) == 0:
            raise ValueError("Config is empty")

        self._config = config

        self._aug_v_models = {}
        self._augs_list = {}
        for category, augs in self._config.items():
            self._augs_list[category] = list(augs.keys())
            self._aug_v_models[category] = {}
            for aug_name, info in augs.items():
                self._aug_v_models[category][aug_name] = {}
                for param in info["params"]:
                    self._aug_v_models[category][aug_name][param["pname"]] = param["default"]

        self._category = list(self._config.keys())[0]
        self._method = list(self._config[self._category].keys())[0]
        self._sometimes = False
        self._probability = 0.5
        self._params = self._config[self._category][self._method]["params"]

        super().__init__(widget_id=widget_id, file_path=__file__)

    def get_json_data(self):
        return {"config": self._config, "augs": self._augs_list}

    def get_json_state(self):
        return {
            "category": self._category,
            "name": self._method,
            "sometimes": self._sometimes,
            "probability": self._probability,
            "params": self._params,
            "augVModels": self._aug_v_models,
        }

    def get_config(self):
        return self._config

    def get_category(self):
        return StateJson()[self.widget_id]["category"]

    def get_method(self):
        return StateJson()[self.widget_id]["name"]

    def get_probability(self):
        sometimes = StateJson()[self.widget_id]["sometimes"]
        if sometimes:
            return StateJson()[self.widget_id]["probability"]
        else:
            return False

    def get_params(self):
        category = self.get_category()
        method = self.get_method()
        return StateJson()[self.widget_id]["augVModels"][category][method]

    def get_aug_info(self):
        return {
            "category": self.get_category(),
            "name": self.get_method(),
            "probability": self.get_probability(),
            "params": self.get_params(),
        }
