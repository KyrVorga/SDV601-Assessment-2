from model.user import User
from view.register_view import RegisterView
import PySimpleGUI as sg
import sys
sys.dont_write_bytecode = True

# from .login_controller import LoginController


class RegisterController:
    def __init__(self, session):
        self.session = session
        self.view = RegisterView()

    def run(self):
        try:
            self.view.is_closed = False

            while True:
                event, values = self.window.read()
                if event == sg.WIN_CLOSED or event == "Cancel":
                    break
                elif event == "Register":
                    username = values[0]
                    password = values[1]

                    # Check if the username is already taken
                    if User.user_exists(username):
                        sg.popup_error("Username already taken")
                        continue

                    user = User(username, password)
                    user.save()
                    sg.popup("Registration successful")
                    self.window.close()

            self.window.close()

        except Exception as e:
            print(e)
            self.window.close()
