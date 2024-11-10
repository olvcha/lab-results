import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen

Builder.load_file(os.path.join(os.path.dirname(__file__), 'login_screen.kv'))


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def switch_to_new_result_screen(self):
        self.manager.current = 'new_result'
