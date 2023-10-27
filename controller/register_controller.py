import PySimpleGUI as sg
# from .login_controller import LoginController
from model.user import User


class RegisterController:
    def __init__(self):
        self.layout = [
            [sg.Text('Register')],
            [sg.Text('Username'), sg.InputText()],
            [sg.Text('Password'), sg.InputText(password_char='*')],
            [sg.Button('Register'), sg.Button('Cancel')]
        ]
        self.window = sg.Window('Register', self.layout)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Register':
                username = values[0]
                password = values[1]
                user = User(username, password)
                user.save()
                sg.popup('Registration successful')
                self.window.close()

        self.window.close()
