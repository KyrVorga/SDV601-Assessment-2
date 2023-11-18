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
        self.update_data_source_list()

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

                    # Update the des's data sources
                    self.des.data = data_source.name
                    self.des.save()

                case "Delete":
                    data_source_name = values["-DATA_SOURCES-"][0]
                    DataSource.find_by_name(data_source_name).delete()
                    # self.des.save()

                case "Load":
                    data_source_name = values["-DATA_SOURCES-"][0]
                    self.des.data = data_source_name
                    self.des.save()

    def watch_for_changes(self):
        """
        Monitors changes in the data_sources collection
        and refreshes the Data Source if a change is detected,
        also updates the view to reflect the changes.
        """
        with self.collection.watch() as stream:
            for change in stream:
                print(self.des._id, change["documentKey"]["_id"])

                match change["operationType"]:
                    case "insert":
                        self.update_data_source_list()
                        self.view.update_data_sources(
                            self.des.data_sources)

                    case "delete":
                        self.update_data_source_list()
                        self.view.update_data_sources(
                            self.des.data_sources)

                    case "update":
                        self.update_data_source_list()
                        self.view.update_data_sources(
                            self.des.data_sources)

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
                    try:
                        data_source_data = pandas.read_csv(
                            data_source_data_path_or_url)
                    except Exception as e:
                        print(f"Error reading local file: {e}")
                        return None, None
                else:
                    # If it's a URL, download it first
                    try:
                        response = requests.get(data_source_data_path_or_url)
                        response.raise_for_status()  # Raise an exception if the download failed
                        data_source_data = pandas.read_csv(
                            io.StringIO(response.text))
                    except Exception as e:
                        print(
                            f"Error downloading or reading file from URL: {e}")
                        return None, None

                window.close()

                # Convert the DataFrame to a list of dictionaries
                data_source_data = data_source_data.to_dict("records")

                return data_source_name, data_source_data
            elif event == "Cancel" or event == sg.WIN_CLOSED:
                window.close()
                return None, None

    def update_data_source_list(self):
        # Fetch all data sources from the database
        data_source_cursor = DataSource.find_by_username(
            self.des.username) or []
        print(data_source_cursor)
        # Convert the cursor to a list of names
        self.available_data_sources = []
        for ds in data_source_cursor:
            self.available_data_sources.append(ds['name'])

        self.view.update_data_sources(self.available_data_sources)
