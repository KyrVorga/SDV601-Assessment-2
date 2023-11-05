import PySimpleGUI as sg
from view.home_view import HomeView
from .login_controller import LoginController
from model.session import Session
import sys
sys.dont_write_bytecode = True


class HomeController:
    """Home controller class"""

    def __init__(self, session):
        self.session = session
        self.view = HomeView()

    def run(self):
        try:
            self.view.is_closed = False

            while True:
                event, values = self.view.read()
                match event:
                    case sg.WIN_CLOSED:
                        break

                    case "Logout":
                        self.session.logout()
                        Session.clear_session_id()
                        self.view.close()
                        login_controller = LoginController(self.session)
                        print("Home - Running login controller")
                        login_controller.run()
                        break

            self.view.close()

        except Exception as e:
            print(e)
            self.view.close()
