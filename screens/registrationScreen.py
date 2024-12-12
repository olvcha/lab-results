import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, \
    MDDialogButtonContainer

from databaseFiles.tables.userTable import UserTable

Builder.load_file(os.path.join(os.path.dirname(__file__), 'registration_screen.kv'))


class RegistrationScreen(Screen):
    '''Handle registration screen actions.'''
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        self.userTable = UserTable()
        self.username = None
        self.password = None
        self.repeat_password = None
        self.register_dialog = None

    def switch_to_login_screen(self):
        self.ids.username_field.text = ""
        self.ids.password_field.text = ""
        self.ids.repeat_password_field.text = ""
        self.ids.register_warning.text = ""
        self.manager.current = 'login'

    def check_fields(self):
        '''Check if registration fields are valid.'''
        username = self.ids.username_field.text
        password = self.ids.password_field.text
        repeat_password = self.ids.repeat_password_field.text
        self.ids.submit_button.disabled = not (username and password and repeat_password)

    def save_user(self):
        '''Save the user to the database with provided data.'''
        self.username = self.ids.username_field.text
        self.password = self.ids.password_field.text
        self.repeat_password = self.ids.repeat_password_field.text
        if self.password == self.repeat_password:
            if self.userTable.get_user(self.username) is None:
                self.userTable.add_user(self.username, self.password)
                self.show_register_dialog()
            else:
                self.ids.register_warning.text = "Użytkownik już istnieje. Spróbuj ponownie."
                self.ids.username_field.text = ""
                self.ids.password_field.text = ""
                self.ids.repeat_password_field.text = ""
        else:
            self.ids.register_warning.text = "Hasła nie są identyczne. Spróbuj ponownie."
            self.ids.password_field.text = ""
            self.ids.repeat_password_field.text = ""

    def show_register_dialog(self):
        self.register_dialog = MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="emoticon",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="Informacja",
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text="Rejestracja przebiegła pomyślnie. Naciśnij \"Powrót\", aby przejść do ekranu logowania.",
                halign="left",
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Powrót"),
                    style="text",
                    on_release=lambda *args: self.register_dialog_action()
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
        )
        self.register_dialog.open()

    def register_dialog_action(self):
        self.register_dialog.dismiss()
        self.switch_to_login_screen()

