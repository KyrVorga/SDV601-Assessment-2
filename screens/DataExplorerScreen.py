from kivy.app import App
from kivy.uix.label import Label


class DataExplorerScreen(App):
    def build(self):
        return Label(text="Hi from DataExplorerScreen")


if __name__ == '__main__':
    DataExplorerScreen().run()
