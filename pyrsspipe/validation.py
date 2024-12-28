from typing_extensions import Self
from pydantic import BaseModel, model_validator, Extra
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
        if not issubclass(validator, BaseModel):
            raise ValueError(f"Module '{module_name}' does not contain 'get_validator' attribute, or it is not callable, or it does not return a pydantic Model")

        return execute, validator


class InputModuleModel(BaseModel, extra = 'allow'):
    module_name: str
    args: dict

    @model_validator(mode='after')
    def deep_validation(self) -> Self:
        self.execute, validator = validate_and_import_module(self.module_name, 'input')
        validator(**self.args)

        return self

class OutputModuleModel(BaseModel, extra = 'allow'):
    module_name: str
    args: dict

    @model_validator(mode='after')
    def deep_validation(self) -> Self:
        self.execute, validator = validate_and_import_module(self.module_name, 'output')
        validator(**self.args)

        return self


class ConfigModel(BaseModel):
    feed_name: str
    feed_language: str
    input: InputModuleModel
    output: OutputModuleModel