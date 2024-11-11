import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file(os.path.join(os.path.dirname(__file__), 'main_screen.kv'))


class MainScreen(Screen):
    '''Handles main screen actions'''
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def switch_to_info_screen(self):
        '''Switches to the info screen'''
        self.manager.current = 'info'

    def switch_to_new_result_screen(self):
        '''Switches to the new result screen'''
        self.manager.current = 'new_result'

    def switch_to_results_screen(self):
        '''Switches to the results screen'''
        self.manager.current = 'results'
