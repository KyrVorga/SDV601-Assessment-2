import PySimpleGUI as sg


class DataExplorerPublicView:
    def __init__(self, name):
        layout = [
            [sg.Text('Enter data to explore:'), sg.Input(key='-DATA-')],
            [sg.Button('Explore'), sg.Button('Cancel')]
        ]
        self.window = sg.Window(name, layout, modal=False, finalize=True)

    def refresh(self):
        self.window.refresh()

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
