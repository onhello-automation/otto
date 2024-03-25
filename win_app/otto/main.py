import sys

from injector import Injector

from otto.configuration import ConfigModule
from otto.listen.listener import OttoListener
from otto.logger import LoggingModule


def main():
    config_path = sys.argv[1]
    inj = Injector([
        ConfigModule(config_path),
        LoggingModule,
    ])
    listener = inj.get(OttoListener)
    listener.listen()


if __name__ == '__main__':
    main()
