import PySimpleGUI as sg

sg.theme('DarkBlue')

login_layout = [
    [sg.Text('Username'), sg.InputText()],
    [sg.Text('Password'), sg.InputText(password_char='*')],
    [sg.Button('Login'), sg.Button('Cancel')],
    [sg.Text("Don't have an account? "), sg.Text(
        'Register', text_color='blue', enable_events=True)]
]

register_layout = [
    [sg.Text('Register')],
    [sg.Text('Username'), sg.InputText()],
    [sg.Text('Password'), sg.InputText(password_char='*')],
    [sg.Button('Register'), sg.Button('Cancel')]
]

login_window = sg.Window('Login', login_layout)

while True:
    event, values = login_window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Login':
        username = values[0]
        password = values[1]
        # TODO: Check username and password against database
        # If valid, close the window and proceed to main app
        # If invalid, show error message and allow user to try again
    elif event == 'Register':
        login_window.hide()
        register_window = sg.Window('Register', register_layout)
        while True:
            event, values = register_window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                break
            elif event == 'Register':
                username = values[0]
                password = values[1]
                # TODO: Add new user to database
                # If successful, close the window and proceed to login screen
                # If unsuccessful, show error message and allow user to try again
        register_window.close()
        login_window.un_hide()

login_window.close()
