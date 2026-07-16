from core.module import Module, ModuleResult


class TestModule(Module):

    def __init__(self):
        super().__init__("TestModule")

    def run(self, state):
        print("[MODULE] Test module executed")

        return ModuleResult.SUCCESS