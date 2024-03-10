from injector import Injector
from otto.listen.listener import OttoListener

from otto.logging_module import LoggingModule


def main():
	inj = Injector([LoggingModule])
	listener = inj.get(OttoListener)
	listener.listen()

if __name__ == '__main__':
	main()