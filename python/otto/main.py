import sys

from injector import Injector

from otto.ai.sk import SKModule
from otto.configuration import ConfigModule
from otto.listen.listener import OttoListener
from otto.logger import LoggingModule


def main():
    config_path = sys.argv[1]
    inj = Injector([
        ConfigModule(config_path),
        LoggingModule,
        SKModule,
    ])
    listener = inj.get(OttoListener)
    listener.listen()


if __name__ == '__main__':
    main()
