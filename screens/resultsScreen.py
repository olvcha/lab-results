import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file(os.path.join(os.path.dirname(__file__), 'results_screen.kv'))


class ResultsScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultsScreen, self).__init__(**kwargs)

    def switch_to_main_screen(self):
        self.manager.current = 'main'

    def switch_to_result_selection_screen(self):
        self.manager.current = 'result_selection'

    def switch_to_parameter_selection_screen(self):
        self.manager.current = 'parameter_selection'