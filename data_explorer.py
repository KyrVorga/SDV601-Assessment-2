import PySimpleGUI as sg
from controller.data_explorer_controller import DataExplorerController
import pickle


def run_des_controller(des):

    # Create a new Data explorer controller
    des_controller = DataExplorerController(des)

    # Run the Data explorer controller
    des_controller.run()


if __name__ == "__main__":
    # Load the pickled DES object from a file
    with open('des.pkl', 'rb') as f:
        des = pickle.load(f)

    run_des_controller(des)
