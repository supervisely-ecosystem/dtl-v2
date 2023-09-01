# coding: utf-8

import json
import os.path

from jsonschema import Draft4Validator, validators

def json_dump(obj, fpath, indent=False):
    indent = 4 if indent else None
    with open(fpath, 'w') as fp:
        json.dump(obj, fp, indent=indent)


def json_load(path):
    try:
        res = json.load(open(path, 'r', encoding='utf-8'))
    except Exception:
        raise RuntimeError('The data in file {} is bad'.format(path))
    return res


def json_dumps(obj):
    return json.dumps(obj)


def json_loads(s):
    return json.loads(s, encoding='utf-8')


class JsonConfigRW:
    def __init__(self, config_fpath):
        self._config_fpath = config_fpath

    @property
    def config_fpath(self):
        return self._config_fpath

    @property
    def config_exists(self):
        return os.path.isfile(self.config_fpath)

    def save(self, config):
        json_dump(config, self.config_fpath)

    def load(self):
        return json_load(self.config_fpath)


# may not work as expected, hm
def _extend_with_default(validator_class):
    validate_properties = validator_class.VALIDATORS["properties"]

    def set_defaults(validator, properties, instance, schema):
        for prop, subschema in properties.items():
            if "default" in subschema:
                instance.setdefault(prop, subschema["default"])

        for error in validate_properties(validator, properties, instance, schema,):
            yield error

    return validators.extend(
        validator_class, {"properties": set_defaults},
    )


def _split_schema(src_schema):
    top_lvl = set(src_schema.keys()) - {'definitions'}

    def get_subschema(key):
        subs = src_schema[key].copy()
        subs.update({'definitions': src_schema['definitions']})
        return subs

    res = {k: get_subschema(k) for k in top_lvl}
    return res


class MultiTypeValidator(object):
    def __init__(self, schema_fpath):
        if not os.path.isfile(schema_fpath):
            self.full_schema = self.subschemas = self.concrete_vtors = None
            return

        vtor_class = _extend_with_default(Draft4Validator)
        self.full_schema = json_load(schema_fpath)
        self.subschemas = _split_schema(self.full_schema)
        self.concrete_vtors = {k: vtor_class(v) for k, v in self.subschemas.items()}

    def val(self, type_name, obj):
        if self.concrete_vtors is None:
            raise RuntimeError('JSON validator is not defined. Type: {}'.format(type_name))
        try:
            self.concrete_vtors[type_name].validate(obj)
        except Exception as e:
            raise RuntimeError('Error occurred during JSON validation. Type: {}. Exc: {}. See documentation'.format(
                type_name, str(e)
            )) from None  # suppress previous stacktrace, save all required info


class SettingsValidator:
    validator = MultiTypeValidator('/workdir/src/schemas.json')

    @classmethod
    def validate_train_cfg(cls, config):
        # store all possible requirements in schema, including size % 16 etc
        cls.validator.val('training_config', config)

    @classmethod
    def validate_inference_cfg(cls, config):
        # store all possible requirements in schema
        cls.validator.val('inference_config', config)

class AlwaysPassingValidator:
    @classmethod
    def validate_train_cfg(cls, config):
        pass

    @classmethod
    def validate_inference_cfg(cls, config):
        pass