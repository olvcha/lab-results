import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from databaseFiles.tables.userTable import UserTable

Builder.load_file(os.path.join(os.path.dirname(__file__), 'registration_screen.kv'))


class RegistrationScreen(Screen):
    '''Handle registration screen actions.'''
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        self.userTable = UserTable()
        self.username = None
        self.password = None

    def switch_to_login_screen(self):
        '''Switch to login screen.'''
        self.ids.username_field.text = ""
        self.ids.password_field.text = ""
        self.ids.register_warning.text = ""
        self.manager.current = 'login'

    def check_fields(self):
        '''Check if registration fields are valid.'''
        username = self.ids.username_field.text
        password = self.ids.password_field.text
        self.ids.submit_button.disabled = not (username and password)

    def save_user(self):
        '''Save the user to the database with provided data.'''
        self.username = self.ids.username_field.text
        self.password = self.ids.password_field.text
        if self.userTable.get_user(self.username) is None:
            self.userTable.add_user(self.username, self.password)
            self.switch_to_login_screen()
        else:
            self.ids.register_warning.text = "Użytkownik już istnieje. Spróbuj ponownie."
            self.ids.username_field.text = ""
            self.ids.password_field.text = ""

