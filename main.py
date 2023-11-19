import PySimpleGUI as sg
from controller.login_controller import LoginController
from controller.home_controller import HomeController
import os
from model.session import Session
from model.database import Database
from model.user import User
from dotenv import load_dotenv
import sys
sys.dont_write_bytecode = True

load_dotenv()


# class MainController:
#     def __init__(self):
#         self.controllers = {}
#         self.session = Session()
#         self.session_id = self.session.get_session_id()

#     def run(self):
#         while True:
#             window, event, values = sg.read_all_windows()

#             if event == sg.WIN_CLOSED or event == 'Exit':
#                 break

#             # Find the controller associated with the window that generated the event
#             active_controller = None
#             for controller in self.controllers.values():
#                 if window == controller.view.window:
#                     active_controller = controller
#                     break

#             # Handle the event with the active controller
#             if active_controller is not None:
#                 active_controller.handle_event(event, values)

#         for controller in self.controllers.values():
#             controller.view.close()

#     def add_controller(self, name, controller):
#         self.controllers[name] = controller

#     def remove_controller(self, name):
#         if name in self.controllers:
#             self.controllers[name].view.close()
#             del self.controllers[name]


# if __name__ == "__main__":
#     main_controller = MainController()
#     # Run the main controller
#     main_controller.run()

#     session = Session()
#     session_id = session.get_session_id()

#     # Check if the user's session ID is stored
#     if session_id:
#         # Find the user with the stored session ID
#         user = User.find_by_session_id(session_id)

#         # If the user exists, log them in
#         if user:
#             session.logged_in = True
#             session.user = user
#         # Else there isn't a user with the stored session ID
#         else:
#             session.logged_in = False
#             session.user = None
#             session.clear_session_id()

#             # Run the login controller
#             login_controller = LoginController(session)
#             main_controller.add_controller('login', login_controller)

#     # Else there isn't a stored session ID
#     else:
#         session.logged_in = False
#         session.user = None

#         # Run the login controller
#         login_controller = LoginController(session)
#         main_controller.add_controller('login', login_controller)

#     # home_controller = HomeController(session)
#     # main_controller.add_controller('home', home_controller)


def main():
    # db = Database(os.getenv("MONGO_URI"))
    session = Session()
    session_id = session.get_session_id()

    # Check if the user's session ID is stored
    if session_id:
        # Find the user with the stored session ID
        user = User.find_by_session_id(session_id)

        # If the user exists, log them in
        if user:
            session.logged_in = True
            session.user = user
        # Else there isn't a user with the stored session ID
        else:
            session.logged_in = False
            session.user = None
            session.clear_session_id()

            # Run the login controller
            login_controller = LoginController(session)
            login_controller.run()

    # Else there isn't a stored session ID
    else:
        session.logged_in = False
        session.user = None

        # Run the login controller
        login_controller = LoginController(session)
        login_controller.run()

    print("Main - Session status:", session.status)
    if session.logged_in:
        home_controller = HomeController(session)
        # If the user is logged in, run the home controller
        print("Starting loop")
        while session.status:
            home_controller.run()
            # home_controller.view.un_hide()
            # home_controller.create_window()

        # session.logout(False)

        print("Session status:", session.status)
        print("Exiting")


if __name__ == "__main__":
    main()
