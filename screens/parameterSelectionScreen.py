import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file(os.path.join(os.path.dirname(__file__), 'parameter_selection_screen.kv'))


class ParameterSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super(ParameterSelectionScreen, self).__init__(**kwargs)
