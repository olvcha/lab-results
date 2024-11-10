from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivymd.app import MDApp

from kivy.uix.screenmanager import ScreenManager
from screens.loginScreen import LoginScreen
from screens.resultScreen import ResultScreen
from screens.newResultScreen import NewResultScreen


class LabResultsApp(MDApp):

    def build(self):
        sm = ScreenManager()
        self.theme_cls.primary_palette = "Royalblue"
        sm.add_widget(LoginScreen(name="login"))
        #sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(ResultScreen(name="result"))
        sm.add_widget(NewResultScreen(name="new_result"))
        return sm


if __name__ == '__main__':
    LabResultsApp().run()
