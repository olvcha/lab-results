import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from databaseFiles.tables.userTable import UserTable

Builder.load_file(os.path.join(os.path.dirname(__file__), 'login_screen.kv'))


class LoginScreen(MDScreen):
    '''Handles login screen actions'''
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.userTable = UserTable()

    def switch_to_main_screen(self):
        '''Switches to the main screen'''
        self.manager.current = 'main'

    def switch_to_registration_screen(self):
        '''Switches to the registration screen'''
        self.manager.current = 'registration'
        self.ids.username_field.text = ""
        self.ids.password_field.text = ""

    def check_fields(self):
        '''Checks if registration fields are valid'''
        username = self.ids.username_field.text
        password = self.ids.password_field.text
        self.ids.submit_button.disabled = not (username and password)

    def auth_user(self):
        '''Authorizes the user. If data is correct, the user will be redirected to the main screen.
        If not, the error will be displayed'''
        username = self.ids.username_field.text
        password = self.ids.password_field.text
        authorization = self.userTable.auth_user(username, password)

        if authorization is not False:
            self.on_login(authorization)
            self.switch_to_main_screen()
        else:
            self.ids.username_field.text = ""
            self.ids.password_field.text = ""

    def on_login(self, user_id):
        '''Handles actions upon successfully logged in'''
        app = MDApp.get_running_app()
        app.set_user_id(user_id)




