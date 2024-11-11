import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file(os.path.join(os.path.dirname(__file__), 'result_selection_screen.kv'))


class ResultSelectionScreen(Screen):
    '''Handles result screen actions'''
    def __init__(self, **kwargs):
        super(ResultSelectionScreen, self).__init__(**kwargs)

    def switch_to_results_screen(self):
        '''Switches to the results screen'''
        self.manager.current = 'results'