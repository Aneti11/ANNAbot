from core.module import Module, ModuleResult


class M0040CheckCharacter(Module):

    def __init__(self):
        super().__init__(
            "CheckCharacter",
            module_type="system"
        )


    def run(self, context):

        character = context.game.get_current_character()

        print(f"[GAME] Current character: {character}")

        return ModuleResult.SUCCESS