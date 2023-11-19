import PySimpleGUI as sg


class DataSourceManagerView:
    def __init__(self, data_sources=[]):
        layout = [
            [sg.Text('Data Sources')],
            [sg.Listbox(values=data_sources, size=(30, 6),
                        key='-DATA_SOURCES-', enable_events=True)],
            [sg.Button('Load'), sg.Button('Add'),
             sg.Button('Merge'), sg.Button('Delete')]
        ]
        self.window = sg.Window('Data Source Manager', layout, finalize=True)

    def update_data_sources(self, data_sources):
        self.window['-DATA_SOURCES-'].update(data_sources)

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
