import PySimpleGUI as sg
import sys
sys.dont_write_bytecode = True


class HomeView():
    """Home view class"""

    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Text("Welcome to the home page")],
            [sg.Button("Logout")]
        ]

        self.window = sg.Window("Home", self.layout)
        self.is_closed = False

    def read(self):
        return self.window.read()

    def close(self):
        self.is_closed = True
        self.window.close()

    def hide(self):
        self.window.hide()

    def un_hide(self):
        self.window.un_hide()

    def show_error(self, message):
        sg.popup_error(message)

    def show_message(self, message):
        sg.popup(message)
