import PySimpleGUI as sg


class DataExplorerView:
    def __init__(self, name, chat='', public_state=False):

        self.chat = ''
        for message in chat:
            self.chat += message + '\n'

        chat_layout = [
            [sg.Multiline(size=(40, 20), disabled=True,
                          autoscroll=True, key='-OUTPUT-')],
            [sg.Input(size=(35, 5),
                      key='-CHAT-', do_not_clear=False)],
            [sg.Button('Send', bind_return_key=True)]
        ]

        explorer_layout = [
            [sg.Button('Manage Data Source'), sg.Button('Chart Settings'),
             sg.Checkbox('Make Public', key='-PUBLIC-', enable_events=True, default=public_state)],
            [sg.Canvas(size=(40, 40), key='-CANVAS-')],
            [sg.Canvas(size=(40, 5), key='-CANVAS_TOOLS-')],
        ]

        layout = [
            [sg.Column(explorer_layout), sg.Column(chat_layout)]
        ]

        self.window = sg.Window(name, layout, modal=False, finalize=True)
        self.window['-OUTPUT-'].update(self.chat, append=True)
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
