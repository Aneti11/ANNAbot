from core.module import Module, ModuleResult


class M00Test(Module):

    def __init__(self):
        super().__init__("M00Test")


    def run(self, state):
        print("[MODULE] Test module executed")

        return ModuleResult.SUCCESS