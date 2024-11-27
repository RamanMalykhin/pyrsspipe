# validation.py

from pydantic import BaseModel, validator, ValidationError
import importlib

def import_module(module_name: str):
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError:
        raise ValidationError(f"Module '{module_name}' could not be imported")

class ConfigModel(BaseModel):
    input_module: str
    output_module: str

    @validator('input_module', 'output_module', pre=True)
    def validate_and_import_module(cls, value):
        module = import_module(value)
        callable = getattr(module, 'execute', None)
        if callable is None:
            raise ValidationError(f"Module '{value}' does not contain 'execute' method")
        cls.execute = callable