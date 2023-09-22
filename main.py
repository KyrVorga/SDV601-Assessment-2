from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem

from screens.LoginScreen import LoginScreen
from screens.HomeScreen import HomeScreen

from kivy import Config

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '600')

Config.set('graphics', 'minimum_width', '300')
Config.set('graphics', 'minimum_height', '250')


class HomepageApp(MDApp):
    def build(self):
        screen_manager = ScreenManager(transition=FadeTransition(duration=0.1))
        screen_manager.add_widget(LoginScreen(name='login'))
        screen_manager.add_widget(HomeScreen(name='home'))
        return screen_manager

    def on_start(self):
        for i in range(20):
            (self.root.screens[1].ids.des_instances.add_widget(
                OneLineListItem(text=f"Single-line item {i}")
            ))


if __name__ == '__main__':

    Builder.load_file("screens/LoginScreen.kv")
    Builder.load_file("screens/HomeScreen.kv")
    HomepageApp().run()
