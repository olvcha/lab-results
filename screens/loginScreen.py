import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from databaseFiles.tables.userTable import UserTable
from implementation.globalData import GlobalData

Builder.load_file(os.path.join(os.path.dirname(__file__), 'login_screen.kv'))


class LoginScreen(Screen):
    '''Handle login screen actions'''
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.userTable = UserTable()

    def on_enter(self):
        self.ids.username_field.text = ""
        self.ids.password_field.text = ""
        self.ids.login_warning.text = ""

    def switch_to_main_screen(self):
        '''Switch to the main screen'''
        self.manager.current = 'main'

    def switch_to_registration_screen(self):
        '''Switch to the registration screen'''
        self.manager.current = 'registration'
        self.ids.username_field.text = ""
        self.ids.password_field.text = ""

    def check_fields(self):
        '''Check if registration fields are valid.'''
        username = self.ids.username_field.text
        password = self.ids.password_field.text
        self.ids.submit_button.disabled = not (username and password)

    #to-do: error
    def auth_user(self):
        '''Authorize the user. If data is correct, the user will be redirected to the main screen.
        If not, the error will be displayed'''
        username = self.ids.username_field.text
        password = self.ids.password_field.text
        authorization = self.userTable.auth_user(username, password)

        if authorization is not False:
            self.on_login(authorization)
            self.switch_to_main_screen()
            self.ids.login_warning.text = ""
        else:
            self.ids.username_field.text = ""
            self.ids.password_field.text = ""
            self.ids.login_warning.text = "Nieprawidłowe dane. Spróbuj ponownie."

    def on_login(self, user_id):
        '''Handle actions upon successfully logging in, in that case it is setting the logged user's id'''
        global_data = GlobalData()
        global_data.set_user_id(user_id)



