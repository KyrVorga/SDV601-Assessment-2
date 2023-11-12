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
sys.dont_write_bytecode = True


class HomeController:
    """Home controller class"""

    def __init__(self, session):
        self.session = session

        # Fetch all data explorers from the database
        data_explorers_cursor = DataExplorer.find_available_des(
            self.session.user.username)

        # Convert the cursor to a list of names
        data_explorers = []
        for des in data_explorers_cursor:
            data_explorers.append(des['name'])

        print("Data Explorers:", data_explorers)

        self.view = HomeView(data_explorers)
        self.new_des = NewDesView()

    def run(self):
        try:
            while True:
                event, values = self.view.read()

                match event:
                    case sg.WIN_CLOSED:
                        self.session.status = False
                        # print("Home - Session Status:", self.session.status)
                        break

                    case "Logout":
                        self.session.logout()
                        Session.clear_session_id()
                        self.view.close()
                        login_controller = LoginController(self.session)
                        # print("Home - Running login controller")
                        login_controller.run()
                        break

                    case "Load DES":
                        print("Loading DES")
                        if len(values['-LIST-']) == 0:
                            sg.popup_error("You must select a DES first")
                            break
                        # Get the selected DES name from the list
                        selected_des = values['-LIST-'][0]

                        # Find the DES object with the selected name
                        des = DataExplorer.find_by_name(selected_des)

                        # Serialize the DES object
                        with open('des.pkl', 'wb') as f:
                            pickle.dump(des, f)

                        # Start the Data Explorer application
                        subprocess.Popen(
                            ["python", "data_explorer.py"])

                    case "New DES":
                        event, values = self.new_des.read()
                        print(event, values)
                        if event == "Create":
                            print("Creating new DES")

                            # Define the fields of the new DES
                            des_name = values["-NAME-"]
                            username = self.session.user.username
                            des_id = DataExplorer.generate_des_id()

                            # Check if the DES name is already taken
                            if DataExplorer.des_exists(des_name):
                                sg.popup_error("DES name already taken")
                                break

                            # Create the new DES object
                            new_des = DataExplorer(des_name, username, des_id)

                            # Save the new DES to the database
                            new_des.save()

                            # Update the DES list
                            self.des_list = DataExplorer.find_available_des(
                                self.session.user.username)

                            self.new_des.close()
                            break
                        elif event == "Cancel":
                            self.new_des.close()
                            break
                        break

            self.view.close()

        except Exception as e:
            print(e)
            self.view.close()
