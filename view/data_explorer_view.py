import PySimpleGUI as sg


class DataExplorerView:
    def __init__(self, name, public_state=False):
        layout = [
            [sg.Text('Enter data to explore:'), sg.Input(key='-DATA-')],
            [sg.Button('Explore'), sg.Button('Cancel'),
             sg.Checkbox('Make Public', key='-PUBLIC-', enable_events=True, default=public_state)]
        ]
        self.window = sg.Window(name, layout, modal=False, finalize=True)
        self._public_state = public_state

    @property
    def public_state(self):
        return self._public_state

    @public_state.setter
    def public_state(self, value):
        self._public_state = value
        self.window['-PUBLIC-'].update(value)

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
