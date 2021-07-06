import json


def process_config(config_path):
    def _read_json(path):
        with open(path, "r") as f:
            return json.load(f)

    if config_path is None:
        return None, None

    config = None

    try:
        config = _read_json(config_path)
    except Exception as e:
        print(
            "Config file-read error encountered with exception {}\nIgnoring config file for now.".format(
                e
            )
        )
        config = None

    if config is None:
        return None, None

    cpu, ram = None, None

    if "cpu" in config:
        cpu = config["cpu"]

    if "ram" in config:
        ram = config["ram"]

    return cpu, ram
