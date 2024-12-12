from kivy.config import Config

Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivymd.app import MDApp
from screens.appScreenManager import AppScreenManager
from databaseFiles.databaseInitialization import DatabaseInitialization


class LabResultsApp(MDApp):

    def build(self):
        '''Build the app'''
        self.theme_cls.primary_palette = "Indigo"
        db = DatabaseInitialization()
        db.initialize()

        return AppScreenManager()


if __name__ == '__main__':
    LabResultsApp().run()
