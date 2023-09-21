from kivy.app import App
from kivy import Config
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout

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


class DataExplorerApp(App):
    def build(self):
        return DataExplorer()

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': f'Instance {i}'} for i in range(1, 4)]


if __name__ == '__main__':
    # Builder.load_file("screens/DataExplorerApp.kv")
    DataExplorerApp().run()
