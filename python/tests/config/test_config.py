from injector import Injector

from otto.configuration import Config, ConfigModule
from otto.logger import LoggingModule


def test_config_module():
    inj = Injector([
        ConfigModule('sample_config.yaml'),
        LoggingModule,
    ])
    config = inj.get(Config)
    assert config.log_level in ('DEBUG', 'INFO')
    assert config.sk is not None
