import os
from model.database import Database
from view.data_explorer_view import DataExplorerView
import PySimpleGUI as sg
import threading


class DataExplorerController:

    collection = Database(os.getenv("MONGO_URI")).get_collection(
        "mydatabase", "data_explorers")

    def __init__(self, des):
        # self.username = username
        self.des = des
        self.view = DataExplorerView(self.des.name, self.des.is_public)

    def run(self):

        def watch():
            self.watch_for_changes()

        thread = threading.Thread(target=watch)
        thread.start()

        while True:
            event, values = self.view.read()
            print(event, values)
            match event:
                case sg.WIN_CLOSED:
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

    def watch_for_changes(self):
        """
            Monitors changes in the data_explorer collection
            and refreshes the Data Explorer if a change is detected,
            also updates the DES view to reflect the changes.
        """
        with self.collection.watch() as stream:
            for change in stream:
                # if change["documentKey"]["des_id"] == self.des.des_id:
                #     self.des.refresh()
                #     self.view.update(self.des.name, self.des.is_public)
                print("Change:", change)
                self.des.refresh()
