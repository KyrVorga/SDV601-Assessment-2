import PySimpleGUI as sg
from .register_controller import RegisterController
from model.user import User
from model.session import Session
import bcrypt


class LoginController:
    def __init__(self):
        self.layout = [
            [sg.Text("Username"), sg.InputText()],
            [sg.Text("Password"), sg.InputText(password_char="*")],
            [sg.Button("Login"), sg.Button("Cancel")],
            [sg.Text("Don't have an account? "), sg.Text(
                "Register", text_color="blue", enable_events=True)]
        ]
        self.window = sg.Window("Login", self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == "Cancel":
                break
            elif event == "Login":
                username = values[0]
                password = values[1]

                user = User.find_by_username(username)
                # Check if password matches hashed value
                if bcrypt.checkpw(password.encode("utf-8"), user.password):
                    sg.popup("Password matches")
                else:
                    sg.popup("Invalid username or password")

                # if user and user.password == password:
                #     session = Session(user._id, "some_token")
                #     session.save()
                #     self.window.close()
                #     # TODO: Open main app window
                # else:

            elif event == "Register":
                self.window.hide()
                register_controller = RegisterController()
                register_controller.run()
                self.window.un_hide()

        self.window.close()
