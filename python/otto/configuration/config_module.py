import logging
from logging import Logger

from dacite import from_dict
from injector import Module, provider, singleton
from yaml import safe_load

from otto.ai.sk import SKConfig
from otto.configuration import Config


class ConfigModule(Module):
    def __init__(self, config_path: str):
        self._path = config_path

    @provider
    @singleton
    def provide_config(self, logger: Logger) -> Config:
        logger.info("Loading configuration from \"%s\".", self._path)
        with open(self._path, 'r', encoding='utf-8') as f:
            config = safe_load(f)
        result = from_dict(Config, config)

        if result.log_level is not None:
            logger.setLevel(result.log_level)

        if result.global_log_level is not None:
            logging.basicConfig(level=result.global_log_level)

        return result

    @provider
    @singleton
    def provide_sk_config(self, config: Config) -> SKConfig:
        return config.sk
