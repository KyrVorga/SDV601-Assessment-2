import io
import os
from model.data_source import DataSource
from model.database import Database
from view.data_source_manager_view import DataSourceManagerView
import PySimpleGUI as sg
import threading
import requests
import pandas


class DataSourceController:
    db = Database.getInstance()
    collection = db.get_collection("data_sources")

    def __init__(self, des):
        self.des = des
        self.view = DataSourceManagerView()

    def run(self):
        def watch():
            self.watch_for_changes()

        thread = threading.Thread(target=watch, daemon=True)
        thread.start()

        while True:
            event, values = self.view.read()
            print(event, values)
            match event:
                case sg.WIN_CLOSED:
                    os._exit(0)

                case "Cancel":
                    break

                case "Add":
                    # Open modal to gather data source name and data
                    data_source_name, data_source_data = self.open_data_source_modal()

                    # Create a new DataSource object
                    data_source = DataSource(
                        data_source_name, self.des.username, None, data_source_data)

                    # Save the data source
                    data_source.save()

                    # Update the user's data sources
                    self.des.data_source = data_source._id
                    self.des.save()

                    # Update the view to reflect the changes
                    self.view.update_data_sources(self.des.data_sources)
                    self.view.clear_input()

                case "Delete":
                    data_source_id = values["-DATA_SOURCES-"][0]
                    self.des.data_sources.remove(data_source_id)
                    self.des.save()
                    self.view.update_data_sources(self.des.data_sources)
                    self.view.clear_input()

    def watch_for_changes(self):
        """
        Monitors changes in the data_sources collection
        and refreshes the Data Source if a change is detected,
        also updates the view to reflect the changes.
        """
        with self.collection.watch() as stream:
            for change in stream:
                print(self.des._id, change["documentKey"]["_id"])

    def open_data_source_modal(self):
        layout = [
            [sg.Text("Data Source Name:")],
            [sg.Input(key="-NAME-")],
            [sg.Text("Upload a .csv")],
            [sg.Input(key="-DATA-"), sg.FileBrowse()],
            [sg.Button("OK"), sg.Button("Cancel")]
        ]

        window = sg.Window("Add Data Source", layout)

        while True:
            event, values = window.read()
            if event == "OK":
                data_source_name = values["-NAME-"]
                data_source_data_path_or_url = values["-DATA-"]

                if os.path.isfile(data_source_data_path_or_url):
                    # If it's a local file, read it directly
                    data_source_data = pandas.read_csv(
                        data_source_data_path_or_url)
                else:
                    # If it's a URL, download it first
                    response = requests.get(data_source_data_path_or_url)
                    response.raise_for_status()  # Raise an exception if the download failed
                    data_source_data = pandas.read_csv(
                        io.StringIO(response.text))

                window.close()
                return data_source_name, data_source_data
            elif event == "Cancel" or event == sg.WIN_CLOSED:
                window.close()
                return None, None
