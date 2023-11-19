import PySimpleGUI as sg
import sys
sys.dont_write_bytecode = True


class HomeView():
    """Home view class"""

    # def __init__(self, des_list=[]):
    #     sg.theme("DarkBlue")

    #     self.layout = [
    #         [sg.Text("Welcome to the home page"), sg.Button("Logout")],
    #         [sg.Listbox(values=des_list, size=(40, 10), key='-LIST-')],
    #         [sg.Button("Load DES"), sg.Button(
    #             "New DES"), sg.Button("Delete DES")],
    #     ]

    #     self.window = sg.Window("Home", self.layout)

    def __init__(self):
        sg.theme("DarkBlue")

        self.layout = [
            [sg.Text("Welcome to the home page"), sg.Button("Logout")],
            [sg.Listbox(values=[], size=(40, 10), key='-LIST-')],
            [sg.Button("Load DES"), sg.Button(
                "New DES"), sg.Button("Delete DES")],
        ]

        self.window = sg.Window("Home", self.layout, finalize=True)

    def update_des_list(self, des_list):
        self.window['-LIST-'].update(des_list)

    def read(self):
        return self.window.read()

    def close(self):
        self.window.close()

    def hide(self):
        self.window.hide()

    def un_hide(self):
        self.window.un_hide()

    def show_error(self, message):
        sg.popup_error(message)

    def show_message(self, message):
        sg.popup(message)
