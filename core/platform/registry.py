import winreg


CURRENT_USER = winreg.HKEY_CURRENT_USER
LOCAL_MACHINE = winreg.HKEY_LOCAL_MACHINE


class WindowsRegistry:
    """
    Работа с системным реестром Windows.
    """

    @staticmethod
    def get_value(root, key, value_name):

        try:

            with winreg.OpenKey(root, key) as registry_key:

                value, _ = winreg.QueryValueEx(
                    registry_key,
                    value_name
                )

                return value

        except FileNotFoundError:
            return None


    @staticmethod
    def key_exists(root, key):

        try:

            with winreg.OpenKey(root, key):
                return True

        except FileNotFoundError:
            return False