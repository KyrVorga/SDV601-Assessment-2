from view.data_explorer_view import DataExplorerView
import PySimpleGUI as sg


class DataExplorerController:
    def __init__(self, des):
        # self.username = username
        self.des = des
        self.view = DataExplorerView(self.des.name, self.des.is_public)

    def run(self):

        while True:
            event, values = self.view.read()
            print(event, values)
            match event:
                case sg.WIN_CLOSED:
                    # self.view.close()
                    break

                case "Cancel":
                    break

                case "-PUBLIC-":
                    state = values["-PUBLIC-"]
                    print("State:", state)
                    self.des.toggle_public(state)

                case "Explore":
                    data = values[0]
                    # Add your data exploration logic here

        self.view.close()
