import logging
import os
from logging import Logger

from injector import Module, provider, singleton


class LoggingModule(Module):
    @provider
    @singleton
    def provide_logger(self) -> Logger:
        log_level = os.environ.get('OTTO_LOG_LEVEL', logging.WARNING)
        result = logging.Logger('otto')
        result.setLevel(log_level)
        f = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s:%(filename)s:%(funcName)s\n%(message)s')
        h = logging.StreamHandler()
        h.setFormatter(f)
        result.addHandler(h)
        return result
