import importlib


class ModuleLoader:

    @staticmethod
    def load_modules(path="config/modules.json"):

        import json

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        modules = []

        for module_data in data["modules"]:

            if not module_data["enabled"]:
                continue

            module_name = module_data["name"]

            module_class = ModuleLoader._load_class(
                module_name
            )

            modules.append(
                module_class()
            )

        return modules


    @staticmethod
    def _load_class(module_name):

        module_path = f"modules.{module_name}"

        module = importlib.import_module(
            module_path
        )

        class_name = ModuleLoader._class_name(
            module_name
        )

        return getattr(
            module,
            class_name
        )


    @staticmethod
    def _class_name(module_name):

        parts = module_name.split("_")

        return "".join(
            part.capitalize()
            for part in parts
        )