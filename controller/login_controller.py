from view.login_view import LoginView
from model.session import Session
from model.user import User
import PySimpleGUI as sg
from .register_controller import RegisterController
import sys
sys.dont_write_bytecode = True


class LoginController:
    def __init__(self, session):
        self.session = session
        self.view = LoginView()

    def run(self):
        try:
            self.view.is_closed = False

            while True:
                event, values = self.view.read()
                if event == sg.WIN_CLOSED or event == "Cancel":
                    self.session.status = False
                    break
                elif event == "Login":
                    username = values[0]
                    password = values[1]

                    # attempt to login
                    self.session.login(username, password)
                    self.view.hide()

                    if self.session.logged_in:
                        # Save the session_id to the enviroment variables
                        self.session.save_session_id()
                        self.view.show_message("Login successful")
                        self.view.close()
                        break
                    else:
                        self.view.show_error("Login failed")
                        self.view.un_hide()

                elif event == "Register":
                    self.view.hide()
                    register_controller = RegisterController(self.session)
                    # print("Login - Running register controller")
                    register_controller.run()
                    self.view.un_hide()

            self.view.close()

        except Exception as e:
            print(e)
            self.view.close()
