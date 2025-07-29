import yaml

config: dict

def load_config(config_file: str) -> dict:
    with open(config_file, "r") as file:
        data = yaml.safe_load(file)
    return data