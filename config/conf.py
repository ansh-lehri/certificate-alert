import os
from typing import Dict
from config.logger import logger
import yaml


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class FileConfig:

    def __init__(self, socket_connection_timeout_seconds, warn_if_days_less_than,
                 slack_bot_token=None, slack_channel_id=None):
        self.socket_connection_timeout_seconds = socket_connection_timeout_seconds
        self.warn_if_days_less_than = warn_if_days_less_than
        self.slack_bot_token = slack_bot_token
        self.slack_channel_id = slack_channel_id


class EnvConfig(FileConfig):

    def __init__(self, socket_connection_timeout_seconds, warn_if_days_less_than,
                 slack_bot_token=None, slack_channel_id=None):

        super().__init__(socket_connection_timeout_seconds, warn_if_days_less_than,
                         slack_bot_token, slack_channel_id)
        # Override variables from env
        if "SLACK_BOT_TOKEN" in os.environ:
            self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        if "SLACK_CHANNEL_ID" in os.environ:
            self.slack_channel_id = os.environ.get("SLACK_CHANNEL_ID")


class Config(EnvConfig):
    def __init__(self, config_dict: Dict):
        # Set the values as per config file and override them with env variables
        super().__init__(
            slack_bot_token=config_dict.get("SLACK_BOT_TOKEN", None),
            slack_channel_id=config_dict.get("SLACK_CHANNEL_ID", None),
            socket_connection_timeout_seconds=config_dict.get("SOCKET_CONNECTION_TIMEOUT_SECONDS"),
            warn_if_days_less_than=config_dict.get("WARN_IF_DAYS_LESS_THAN"),
        )
        # Set any extra variables from config file, create python object
        extra_config_dict = {k: v for k, v in config_dict.items() if k not in self.__dict__}
        self.__dict__.update(**extra_config_dict)


config_file_path = os.environ.get("CONFIG_FILE_PATH")


if not config_file_path:
    config_file_path = "%sconfig.yaml" % (os.path.abspath(__file__).rstrip("config.py"))
    logger.info("CONFIG_FILE_PATH not found in env, picking default: %s".format(config_file_path))
else:
    logger.info("CONFIG_FILE_PATH found in env: %s".format(config_file_path))

with open(file=config_file_path, mode="r") as val:
    config_dict_from_file = dict(yaml.safe_load(val))

# update_configs_from_env(config_dict)
config = Config(config_dict_from_file)
