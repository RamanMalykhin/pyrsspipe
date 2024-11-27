
from pydantic import BaseModel, validator, ValidationError
import importlib

def import_module(module_name: str):
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError:
        raise ValidationError(f"Module '{module_name}' could not be imported")

class ConfigModel(BaseModel):
    feed_name: str
    feed_language: str
    input_module: dict
    output_module: dict

    @validator('input_module','output_module', pre=True)
    def validate_and_import_module(cls, value):
        module = import_module(value)
        callable = getattr(module, 'execute', None)
        if callable is None:
            raise ValidationError(f"Module '{value}' does not contain 'execute' method")
        cls.execute = callable
    
    @validator('input_module', 'output_module', pre=True)
    def validate_args(cls, value):
        mandatory = set()
        optional = set()
        
        defined_args = inspect.signature(cls.execute).parameters
        for arg in defined_args.values():
            if arg.default == inspect._empty:
                mandatory.add(arg.name)
            else:
                optional.add(arg.name)
        
        mandatory_missing = mandatory.difference(set(value['args'].keys()))
        optional_missing = optional.difference(set(value['args'].keys()))
        
        if mandatory_missing:
            raise ValueError(f'Missing mandatory arguments: {mandatory_missing}')
        elif optional_missing:
            for arg in optional_missing:
                print(f"Optional argument {arg} missing. Default value {defined_args[arg].default} will be used")
                
        