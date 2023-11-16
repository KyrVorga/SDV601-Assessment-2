import pickle
import subprocess
import PySimpleGUI as sg
from view.home_view import HomeView
from view.new_des_view import NewDesView
from controller.login_controller import LoginController
from controller.data_explorer_controller import DataExplorerController
from model.session import Session
from model.data_explorer import DataExplorer
import sys
import uuid
sys.dont_write_bytecode = True


class HomeController:
    """Home controller class"""

    def __init__(self, session):
        self.session = session

        self.view = HomeView()
        self.new_des_view = NewDesView()

        # Update the DES list
        self.update_des_list()

        self.active_data_explorers = {}

    # def create_window(self):
    #     self.view = HomeView(self.data_explorers)
    #     self.new_des = NewDesView()

    def update_des_list(self):
        # Fetch all data explorers from the database
        data_explorers_cursor = DataExplorer.find_available_des(
            self.session.user.username) or []

        # Convert the cursor to a list of names
        self.data_explorers = []
        for des in data_explorers_cursor:
            self.data_explorers.append(des['name'])

        self.view.update_des_list(self.data_explorers)

    def run(self):
        try:
            while True:
                # Iterate over a copy of the dictionary items
                for des_name, process in list(self.active_data_explorers.items()):
                    if process.poll() is not None:
                        # The process has terminated, so remove it from the dictionary
                        del self.active_data_explorers[des_name]

                event, values = self.view.read()

                match event:
                    case sg.WIN_CLOSED:
                        self.session.status = False
                        for process in self.active_data_explorers.values():
                            process.terminate()
                        break

                    case "Logout":
                        self.session.logout()
                        Session.clear_session_id()
                        self.session.status = False
                        self.view.hide()
                        login_controller = LoginController(self.session)
                        # print("Home - Running login controller")
                        login_controller.run()

                        if self.session.logged_in:
                            self.view.un_hide()
                            self.session.status = True
                        else:
                            self.view.close()

                    case "Load DES":
                        print("Loading DES")
                        if len(values['-LIST-']) == 0:
                            sg.popup_error("You must select a DES first")
                        else:
                            # Get the selected DES name from the list
                            selected_des = values['-LIST-'][0]

                            # Find the DES object with the selected name
                            des = DataExplorer.find_by_name(selected_des)
                            print("DES:", des)

                            # Serialize the DES object
                            with open('des.pkl', 'wb') as f:
                                pickle.dump(des, f)

                            # Start the Data Explorer application
                            process = subprocess.Popen(
                                [sys.executable, "data_explorer.py"])

                            # Store the subprocess in the dictionary using a uuid as the key
                            id = str(uuid.uuid4())
                            self.active_data_explorers[id] = process

                            print("Active Data Explorers:",
                                  self.active_data_explorers)

                    case "New DES":
                        event, values = self.new_des_view.read()
                        print(event, values)
                        if event == "Create":
                            print("Creating new DES")

                            # Define the fields of the new DES
                            des_name = values["-NAME-"]
                            username = self.session.user.username
                            # des_id = DataExplorer.generate_des_id()

                            # Check if the DES name is already taken
                            if DataExplorer.des_exists(des_name):
                                sg.popup_error("DES name already taken")
                            else:
                                # Create the new DES object
                                new_des = DataExplorer(
                                    des_name, username)  # , des_id)

                                # Save the new DES to the database
                                new_des.save()

                                # Update the DES list
                                self.des_list = DataExplorer.find_available_des(
                                    self.session.user.username)

                                self.new_des_view.hide()

                        elif event == "Cancel":
                            self.new_des_view.hide()

                    case "Delete DES":
                        if len(values['-LIST-']) == 0:
                            sg.popup_error("You must select a DES first")
                        else:
                            # Get the selected DES name from the list
                            selected_des = values['-LIST-'][0]

                            # Check the active DES list for the selected DES
                            if selected_des in self.active_data_explorers:
                                # Kill the process
                                self.active_data_explorers[selected_des].kill()

                                # Remove the process from the dictionary
                                del self.active_data_explorers[selected_des]

                            # Find the DES object with the selected name
                            des = DataExplorer.find_by_name(selected_des)

                            # Delete the DES from the database
                            des.delete()

                            # Remove the DES from the list
                            self.des_list = DataExplorer.find_available_des(
                                self.session.user.username)

                    case "Update List":
                        self.update_des_list()

            # self.view.close()

        except Exception as e:
            print(e)
            self.view.close()
