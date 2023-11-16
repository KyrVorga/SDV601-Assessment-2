import os
import PySimpleGUI as sg
from controller.data_explorer_controller import DataExplorerController
import pickle


def run_des_controller(data):

    # Get the DES object from the data dictionary
    des = data["des"]
    username = data["username"]

    # Create a new Data explorer controller
    des_controller = DataExplorerController(des, username)

    # Run the Data explorer controller
    des_controller.run()


if __name__ == "__main__":
    # Load the pickled DES object from a file
    with open('des.pkl', 'rb') as f:
        data = pickle.load(f)

    run_des_controller(data)

    raise SystemExit
