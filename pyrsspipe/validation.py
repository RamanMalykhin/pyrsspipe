
from pydantic import BaseModel, field_validator
import importlib
from abc import ABC

def find_class_by_parent(base_class, module):
    for name in dir(module):
        obj = getattr(module, name)
        if hasattr(obj, '__bases__') and base_class in obj.__bases__:
            return obj
    return None

def validate_and_import_module(module_name: str, subpackage: str):
        basemodule_cls = find_class_by_parent(ABC, importlib.import_module(f"pyrsspipe.{subpackage}.base"))
        requestedmodule_cls = find_class_by_parent(basemodule_cls, importlib.import_module(f"pyrsspipe.{subpackage}.{module_name}"))

        execute = getattr(requestedmodule_cls, 'execute', None)
        validator_getter = getattr(requestedmodule_cls, 'get_validator', None)
        validator = validator_getter() if callable(validator_getter) else None

        if not callable(execute):
            raise ValueError(f"Module '{module_name}' does not contain 'execute' attribute or it is not callable")
        if not isinstance(validator, BaseModel):
            raise ValueError(f"Module '{module_name}' does not contain 'get_validator' attribute, or it is not callable, or it does not return a pydantic Model")

        return execute, validator


class InputModuleModel(BaseModel):
    module_name: str
    args: dict

    @field_validator('module_name', mode='after')
    def validate_and_import_input_module(cls, module_name):
        cls.execute, cls.validator = validate_and_import_module(module_name, 'input')

    @field_validator('args', mode='after')
    def validate_input_args(cls, args):
        cls.validator.model_validate(**args)


class OutputModuleModel(BaseModel):
    module_name: str
    args: dict

    @field_validator('module_name', mode='after')
    def validate_and_import_input_module(cls, module_name):
        cls.execute, cls.validator = validate_and_import_module(module_name, 'output')

    @field_validator('args', mode='after')
    def validate_input_args(cls, args):
        cls.validator.model_validate(**args)

class ConfigModel(BaseModel):
    feed_name: str
    feed_language: str
    input: InputModuleModel
    output: OutputModuleModel