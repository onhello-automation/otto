import logging
import os
from logging import Logger
from typing import Optional, Union

from injector import Module, provider, singleton


class LoggingModule(Module):
    def __init__(self, log_level: Optional[Union[int, str]] = None):
        if log_level is None:
            log_level = os.environ.get('OTTO_LOG_LEVEL', logging.WARNING)
        self._log_level = log_level

    @provider
    @singleton
    def provide_logger(self) -> Logger:
        result = logging.Logger('otto')
        result.setLevel(self._log_level)
        f = logging.Formatter('%(asctime)s [%(levelname)s] - %(name)s:%(filename)s:%(funcName)s\n%(message)s')
        h = logging.StreamHandler()
        h.setFormatter(f)
        result.addHandler(h)
        return result
