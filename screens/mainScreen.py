import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

from implementation.globalData import GlobalData
from databaseFiles.tables.userTable import UserTable
Builder.load_file(os.path.join(os.path.dirname(__file__), 'main_screen.kv'))


class MainScreen(Screen):
    '''Handle main screen actions'''
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.global_data = GlobalData()

    def on_enter(self):
        user_id = self.global_data.get_user_id()
        self.welcome(user_id)

    def welcome(self, user_id):
        user_table = UserTable()
        username = user_table.get_user_by_id(user_id)
        self.ids.welcome_label.text = f"Witaj, {username}!"

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
