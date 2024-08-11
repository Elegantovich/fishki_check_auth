import json
import os

from configs.env_settings import ENV


class Config:

    with open(os.path.join(os.getcwd(), "configs/" "config.json")) as file:
        config = json.load(file)
    DTFORMAT = "%Y-%m-%d_%H:%M:%S"
    url = config[ENV]["url"]
    timeout = config["Timeout"]
    root_path = os.path.abspath(os.getcwd())
