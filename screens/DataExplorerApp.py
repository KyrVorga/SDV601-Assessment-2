from kivy.app import App
from kivy import Config
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineListItem

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'minimum_width', '800')
Config.set('graphics', 'minimum_height', '600')


class DataExplorer(BoxLayout):
    def upload_data_source(self):
        pass

    def set_data_source(self):
        pass

    def chart_settings(self):
        pass

    def configure_data(self):
        pass


class DataExplorerApp(MDApp):
    def build(self):
        return DataExplorer()

    def on_start(self):
        for i in range(20):
            self.root.ids.chat_container.add_widget(
                OneLineListItem(text=f"Single-line item {i}")
            )


if __name__ == '__main__':
    DataExplorerApp().run()
