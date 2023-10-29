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


def main():
    db = Database(os.getenv("MONGO_URI"))
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

    # Else there isn't a stored session ID
    else:
        session.logged_in = False
        session.user = None

        # Run the login controller
        login_controller = LoginController(session)
        login_controller.run()

    while True:
        login_controller = LoginController(session)
        home_controller = HomeController(session)

        if not session.logged_in:
            login_controller.run()
            login_controller.view.is_closed = False

        else:
            home_controller.run()
            home_controller.view.is_closed = False

        if login_controller.view.is_closed and home_controller.view.is_closed:
            break

    # session.clear_session_id()
    # session.user = None
    # session.logged_in = False


if __name__ == "__main__":
    main()
