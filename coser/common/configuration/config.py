import os
from typing import Literal, Optional

import yaml

from loguru import logger

CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.sep.join(CONFIG_PATH.split(os.sep)[0:-3])



def load_config(filename: str = "config.yaml"):
    docker_config_path = os.path.join("/configuration/", filename)
    config_path = (
        os.path.join(CONFIG_PATH, filename)
        if not os.path.isfile(docker_config_path)
        else docker_config_path
    )

    with open(config_path, "r") as f_stream:
        config = yaml.load(f_stream, Loader=yaml.FullLoader)
    
    #path parser
    for module,options in config.items():
        if isinstance(options,str):
            if module.endswith("_path"):
                if not module.startswith((".",os.sep)):
                    config[module]=os.path.join(PROJECT_PATH,options)
        elif isinstance(options,dict):
            for key,value in options.items():
                if key.endswith("_path"):
                    if isinstance(value,str):
                        if not value.startswith((".",os.sep)):
                            options[key]=os.path.join(PROJECT_PATH,value)
    
    return config


# get config and set up log folder
CONFIG = load_config()
CONFIG_LOGGER = load_config(filename="logger.yaml")

LOG_PATH = (
    os.path.join(CONFIG_PATH, CONFIG["log_path"])
    if CONFIG["log_path"].startswith(".")
    else CONFIG["log_path"]
)
os.makedirs(LOG_PATH, exist_ok=True)

def get_logger(logger_name: str):
    if logger_name in CONFIG_LOGGER:
        logger.add(
            os.path.join(LOG_PATH, "{}.log".format(logger_name)),
            filter=lambda record: record["extra"]["task"] == logger_name,
            **CONFIG_LOGGER[logger_name],
        )
        return logger.bind(task=logger_name)
    else:
        CONFIG_LOGGER[logger_name] = {"level": "DEBUG", "rotation": "500 MB"}
        logger.add(
            os.path.join(LOG_PATH, "{}.log".format(logger_name)),
            filter=lambda record: record["extra"]["task"] == logger_name,
            **CONFIG_LOGGER[logger_name],
        )
        out_logger = logger.bind(task=logger_name)
        out_logger.error("This logger '{}' is not defined in logger.yaml.".format(logger_name))
        return logger.bind(task=logger_name)