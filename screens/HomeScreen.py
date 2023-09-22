import subprocess
import sys

from kivymd.uix.screen import MDScreen


class HomeScreen(MDScreen):
    def logout(self):
        self.manager.current = 'login'

    @staticmethod
    def open_data_explorer():
        # Get the path to the Python interpreter running this script
        python_interpreter = sys.executable

        # Launch a new instance of DataExplorerScreen as a separate process
        subprocess.Popen([python_interpreter, 'screens/DataExplorerApp.py'])


