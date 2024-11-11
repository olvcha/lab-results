import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen

Builder.load_file(os.path.join(os.path.dirname(__file__), 'info_screen.kv'))


class InfoScreen(Screen):
    '''Handles actions for info screen'''
    def __init__(self, **kwargs):
        super(InfoScreen, self).__init__(**kwargs)

    def switch_to_main_screen(self):
        '''Switches to the main screen'''
        self.manager.current = 'main'
