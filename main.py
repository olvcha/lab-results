from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivymd.app import MDApp
from screens.appScreenManager import AppScreenManager


class LabResultsApp(MDApp):
    user_id = None

    def build(self):
        '''Builds the app'''
        self.theme_cls.primary_palette = "Indigo"
        return AppScreenManager()

    def set_user_id(self, user_id):
        '''Sets user id'''
        self.user_id = user_id

    def get_user_id(self):
        '''Gets user id'''
        return self.user_id


if __name__ == '__main__':
    LabResultsApp().run()
