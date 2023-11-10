from view.data_explorer_view import DataExplorerView
import PySimpleGUI as sg


class DataExplorerController:
    def __init__(self, session, des):
        self.session = session
        self.des = des
        self.view = DataExplorerView(self.des.name)

    def run(self):
        while True:
            event, values = self.view.read()
            if event == sg.WIN_CLOSED or event == "Cancel":
                break
            elif event == "Explore":
                data = values[0]
                # Add your data exploration logic here

        self.view.close()
