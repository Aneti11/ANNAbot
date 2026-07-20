class Game:

    def is_running(self):
        return True


    def is_main_screen(self):
        return True


    def get_current_character(self):
        return None


    def click(self, x, y):
        print(f"[GAME] Click ({x}, {y})")


    def wait(self, seconds):
        print(f"[GAME] Wait {seconds} sec")


    def screenshot(self):
        print("[GAME] Screenshot")


    def open_window(self, name):
        print(f"[GAME] Open window: {name}")