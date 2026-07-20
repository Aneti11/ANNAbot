from core.module import Module, ModuleResult


class M0000CheckEmulator(Module):

    def __init__(self):
        super().__init__(
            "CheckEmulator",
            module_type="system"
        )


    def run(self, context):

        print("[SYSTEM] Checking emulator")

        if context.environment.check():
            return ModuleResult.SUCCESS

        return ModuleResult.FAILED