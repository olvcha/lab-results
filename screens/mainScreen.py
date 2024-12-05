import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

from implementation.globalData import GlobalData

Builder.load_file(os.path.join(os.path.dirname(__file__), 'main_screen.kv'))


class MainScreen(Screen):
    '''Handle main screen actions'''
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.global_data = GlobalData()

    def on_enter(self):
        user_id = self.global_data.get_user_id()
        print(f"Logged in as User ID: {user_id}")

    def switch_to_info_screen(self):
        '''Switch to the info screen'''
        self.manager.current = 'info'

    def switch_to_new_result_screen(self):
        '''Switch to the new result screen'''
        self.manager.current = 'new_result'

    def switch_to_results_screen(self):
        '''Switch to the results screen'''
        self.manager.current = 'results'

    def log_out(self):
        '''Switch to login screen'''
        global_data = GlobalData()
        global_data.set_user_id(None)
        self.manager.current = 'login'
