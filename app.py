""" Hauptfunktion des PDF ChatBots, mit dem das webbasierte Frontend geladen wird. """
from frontend import Frontend

if __name__ == "__main__":
    frontend = Frontend()
    frontend.show_sidebar()
    frontend.show_main_window()
    