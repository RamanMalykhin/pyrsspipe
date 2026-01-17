import os
import json
from pyrsspipe.validation import validate_and_import_module

def get_validator(module_path):
    subpackage, module_name = module_path.split(".")[-2:]
    _, validator = validate_and_import_module(module_name, subpackage)
    return validator


def generate_example_config(input_module, output_module):
    input_validator = get_validator(f"pyrsspipe.input.{input_module}")
    output_validator = get_validator(f"pyrsspipe.output.{output_module}")

    input_example = input_validator.schema().get("example", {})
    output_example = output_validator.schema().get("example", {})

    return {
        "feed_name": "Example Feed",
        "feed_language": "en-us",
        "input": {
            "module_name": input_module,
            "args": input_example
        },
        "output": {
            "module_name": output_module,
            "args": output_example
        }
    }

def list_available_modules(directory):
    return [
        f[:-3] for f in os.listdir(directory)
        if f.endswith(".py") and f != "__init__.py" and f != "base.py"
    ]

def create_pipeconfig():
    pipeconfig_name = input("Enter the name of the new pipeconfig: ")

    input_modules = list_available_modules(os.path.join(os.path.dirname(__file__), "input"))
    output_modules = list_available_modules(os.path.join(os.path.dirname(__file__), "output"))

    print("Available input modules:")
    for idx, module in enumerate(input_modules, start=1):
        print(f"{idx}. {module}")
    input_choice = int(input("Select an input module by number: ")) - 1
    input_module = input_modules[input_choice]

    print("Available output modules:")
    for idx, module in enumerate(output_modules, start=1):
        print(f"{idx}. {module}")
    output_choice = int(input("Select an output module by number: ")) - 1
    output_module = output_modules[output_choice]

    try:
        config = generate_example_config(input_module, output_module)
        config_path = os.path.join(os.getenv("PYRSSPIPE_PIPECONFIG_DIR"), f"{pipeconfig_name}.json")

        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)

        print(f"Pipeconfig '{pipeconfig_name}' created successfully at {config_path}.")
        print("Please edit the configuration file to customize it for your needs.")
    except Exception as e:
        print(f"Error creating pipeconfig: {e}")

if __name__ == "__main__":
    create_pipeconfig()
