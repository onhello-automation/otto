from injector import Module, singleton

from otto.ai.commander import Commander
from otto.ai.sk.sk_adapter import SemanticKernelAdapter


class SKModule(Module):
    def configure(self, binder):
        binder.bind(Commander, to=SemanticKernelAdapter, scope=singleton)
