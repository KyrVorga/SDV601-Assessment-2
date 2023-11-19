import PySimpleGUI as sg


class NewDesView:
    def __init__(self):
        layout = [
            [sg.Text('Enter the name of the new DES:'),
             sg.Input(key='-NAME-')],
            [sg.Button('Create', bind_return_key=True), sg.Button('Cancel')]
        ]
        self.window = sg.Window('New DES', layout)

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
