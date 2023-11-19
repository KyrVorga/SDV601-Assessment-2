import uuid
from .user import User
from dotenv import load_dotenv
import os
import sys
sys.dont_write_bytecode = True


class Session:
    def __init__(self):
        self.logged_in = False
        self.user = None
        self.status = True

    def login(self, username, password):
        """Attempts to authenticate a user with the given username and password"""
        try:
            user = User.find_by_username(username)

            if user:
                if user.is_logged_in == False:
                    if user.check_password(password):
                        user.is_logged_in = True
                        user.session_id = self.generate_session_id()
                        user.save()

                        self.logged_in = True
                        self.user = user
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        except Exception as e:
            print("Login Error:", e)
            return False

    def logout(self, clear_session_id=True):
        """Logs out the user"""
        try:
            if self.logged_in:
                self.user.is_logged_in = False
                if clear_session_id:
                    self.user.session_id = None
                self.user.save()
                self.logged_in = False
                self.user = None
                print("Session - Logged in:", self.logged_in)
                return True
            else:
                return False
        except Exception as e:
            print("Logout Error:", e)

    @ staticmethod
    def generate_session_id():
        """Generates a unique session ID"""
        return str(uuid.uuid4())

    @ staticmethod
    def get_session_id():
        """Gets the session ID from the environment"""
        try:
            load_dotenv()
            session_id = os.getenv("SESSION_ID")
            print("Session - Getting session ID:", session_id)
            return session_id

        except Exception as e:
            print("Error getting session ID:", e)
            return None

    def save_session_id(self):
        """Saves the session ID to the environment"""
        try:
            print("Session - Saving session ID")
            with open(".env", "a") as f:
                f.write(f"SESSION_ID='{self.user.session_id}'\n")
            os.environ["SESSION_ID"] = self.user.session_id
            return True
        except Exception as e:
            print("Error saving session ID:", e)
            return False

    @ staticmethod
    def clear_session_id():
        """Clears the session ID from the environment"""
        try:
            print("Clearing session ID")
            with open(".env", "r") as f:
                lines = f.readlines()
                print(lines)
            with open(".env", "w") as f:
                for line in lines:
                    if not line.startswith('SESSION_ID='):
                        f.write(line)
            os.environ["SESSION_ID"] = ""
            return True
        except Exception as e:
            print("Error clearing session ID:", e)
            return False
