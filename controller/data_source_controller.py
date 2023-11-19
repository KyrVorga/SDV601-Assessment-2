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

    def __init__(self, des, des_controller):
        self.des = des
        self.des_controller = des_controller
        self.view = DataSourceManagerView()
        self.update_data_source_list()

    def run(self):
        def watch():
            self.watch_for_changes()

        thread = threading.Thread(target=watch, daemon=True)
        thread.start()

        while True:
            event, values = self.view.read()
            # print(event, values)
            match event:
                case sg.WIN_CLOSED:
                    self.view.close()
                    break

                case "Cancel":
                    self.view.close()
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
                    self.view.close()
                    break

                case "Merge":
                    data_source_name = values["-DATA_SOURCES-"][0]
                    data_source = DataSource.find_by_name(data_source_name)
                    new_data = self.open_data_source_modal(False)[1]

                    # Merge the new data with the existing data
                    data_source.data.extend(new_data)

                    # Save the data source
                    data_source.save()

                    # Update the des view
                    self.des_controller.view.window.TKroot.after(
                        0, self.des_controller.plot_data_source)

    def watch_for_changes(self):
        """
        Monitors changes in the data_sources collection
        and refreshes the Data Source if a change is detected,
        also updates the view to reflect the changes.
        """
        print("Watching for changes...")
        with self.collection.watch() as stream:
            for change in stream:
                # print(self.des._id, change["documentKey"]["_id"])

                match change["operationType"]:
                    case "insert":
                        self.update_data_source_list()
                        self.view.update_data_sources(
                            self.available_data_sources)

                    case "delete":
                        self.update_data_source_list()
                        self.view.update_data_sources(
                            self.available_data_sources)

                    case "update":
                        self.update_data_source_list()
                        self.view.update_data_sources(
                            self.available_data_sources)

    def open_data_source_modal(self, require_name=True):
        layout = [
            [sg.Text("Upload a .csv")],
            [sg.Input(key="-DATA-"), sg.FileBrowse()],
            [sg.Button("OK"), sg.Button("Cancel")]
        ]
        if require_name:

            layout.insert(0, [sg.Text("Data Source Name:"),
                              [sg.Input(key="-NAME-")]])

        window = sg.Window("Add Data Source", layout)

        while True:
            event, values = window.read()
            if event == "OK":
                if require_name:
                    data_source_name = values["-NAME-"]
                else:
                    data_source_name = True
                data_source_data_path_or_url = values["-DATA-"]

                # Check if the data source value is empty
                if not data_source_data_path_or_url or not data_source_name:
                    sg.popup_error("Both fields must be provided")
                    continue

                else:
                    if os.path.isfile(data_source_data_path_or_url):
                        # If it's a local file, read it directly
                        try:
                            data_source_data = pandas.read_csv(
                                data_source_data_path_or_url)
                        except Exception as e:
                            print(f"Error reading local file: {e}")
                            break
                    else:
                        # If it's a URL, download it first
                        try:
                            response = requests.get(
                                data_source_data_path_or_url)
                            response.raise_for_status()  # Raise an exception if the download failed
                            data_source_data = pandas.read_csv(
                                io.StringIO(response.text))
                        except Exception as e:
                            print(
                                f"Error downloading or reading file from URL: {e}")
                            break

                    window.close()

                    # Convert the DataFrame to a list of dictionaries
                    data_source_data = data_source_data.to_dict("records")

                    if require_name:
                        return data_source_data
                    else:
                        return data_source_name, data_source_data

            elif event == "Cancel" or event == sg.WIN_CLOSED:
                window.close()
                break

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
