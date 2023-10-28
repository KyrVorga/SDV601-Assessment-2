import PySimpleGUI as sg
from .register_controller import RegisterController
from model.user import User


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

                # Check if password matches
                if user:
                    if user.is_logged_in == False:
                        if user.check_password(password):
                            user.is_logged_in = True
                            user.save()
                            sg.popup("Successfully logged in.")
                            # self.window.close()
                            return True
                        else:
                            sg.popup("Incorrect username or password.")
                    else:
                        sg.popup("User already logged in.")
                else:
                    sg.popup("User does not exist.")

            elif event == "Register":
                self.window.hide()
                register_controller = RegisterController()
                register_controller.run()
                self.window.un_hide()

        self.window.close()
