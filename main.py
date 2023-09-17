from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.lang import Builder

from screens.LoginScreen import LoginScreen
from screens.HomeScreen import HomeScreen


class DataExplorerApp(App):
    def build(self):
        screen_manager = ScreenManager(transition=FadeTransition(duration=0.1))
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(HomeScreen(name='home'))
        return screen_manager


if __name__ == '__main__':

    Builder.load_file("screens/LoginScreen.kv")
    Builder.load_file("screens/HomeScreen.kv")
    DataExplorerApp().run()
