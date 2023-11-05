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
            print("Main1 - Running login controller")
            login_controller.run()

    # Else there isn't a stored session ID
    else:
        session.logged_in = False
        session.user = None

        # Run the login controller
        login_controller = LoginController(session)
        print("Main2 - Running login controller")
        login_controller.run()

        print("Main3 - Logged in:", session.logged_in)

    # If the user is logged in, run the home controller
    while session.logged_in:
        home_controller = HomeController(session)
        print("Main4 - Running home controller")
        home_controller.run()
        print("Main5 - Logged in:", session.logged_in)

        # while not session.logged_in:
        #     home_controller = HomeController(session)
        #     print("Main6 - Running home controller")
        #     home_controller.run()

    # session.clear_session_id()
    # session.user = None
    # session.logged_in = False


if __name__ == "__main__":
    main()
