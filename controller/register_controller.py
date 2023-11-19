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
            # self.view.is_closed = False

            while True:
                event, values = self.view.read()
                match event:
                    case sg.WIN_CLOSED:
                        self.session.status = False
                        break

                    case "Cancel":
                        self.session.status = False
                        break

                    case"Register":
                        username = values[0]
                        password = values[1]

                        # Check if the username is already taken
                        if User.user_exists(username):
                            sg.popup_error("Username already taken")
                            continue

                        user = User(username, password)
                        user.save()
                        sg.popup("Registration successful")
                        self.view.hide()
                        break

            self.view.hide()

        except Exception as e:
            print(e)
            self.view.hide()
