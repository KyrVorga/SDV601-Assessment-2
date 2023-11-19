import PySimpleGUI as sg


class DataExplorerPublicView:
    def __init__(self, name, chat=''):
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
            [sg.Canvas(size=(40, 40), key='-CANVAS-')],
            [sg.Canvas(size=(40, 5), key='-CANVAS_TOOLS-')]
        ]

        layout = [
            [sg.Column(explorer_layout), sg.Column(chat_layout)]
        ]

        self.window = sg.Window(name, layout, modal=False, finalize=True)
        self.window['-OUTPUT-'].update(self.chat, append=True)

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
