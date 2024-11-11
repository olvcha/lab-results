from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivymd.app import MDApp

from kivy.uix.screenmanager import ScreenManager
from screens.loginScreen import LoginScreen
from screens.resultScreen import ResultScreen
from screens.newResultScreen import NewResultScreen
from screens.registrationScreen import RegistrationScreen
from screens.infoScreen import InfoScreen
from screens.mainScreen import MainScreen
from screens.parameterSelectionScreen import ParameterSelectionScreen
from screens.resultSelectionScreen import ResultSelectionScreen
from screens.resultsScreen import ResultsScreen


class LabResultsApp(MDApp):

    def build(self):
        sm = ScreenManager()
        self.theme_cls.primary_palette = "Indigo"
        #sm.add_widget(LoginScreen(name="login"))
        #sm.add_widget(RegistrationScreen(name="registration"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(InfoScreen(name="info"))
        sm.add_widget(ResultsScreen(name="results"))
        sm.add_widget(NewResultScreen(name="new_result"))
        sm.add_widget(ResultScreen(name="result"))
        sm.add_widget(ParameterSelectionScreen(name="parameter_selection"))
        sm.add_widget(ResultSelectionScreen(name="result_selection"))

        return sm


if __name__ == '__main__':
    LabResultsApp().run()
