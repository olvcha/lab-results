from kivy.uix.screenmanager import ScreenManager

from screens.loginScreen import LoginScreen
from screens.registrationScreen import RegistrationScreen
from screens.mainScreen import MainScreen
from screens.infoScreen import InfoScreen
from screens.resultsScreen import ResultsScreen
from screens.newResultScreen import NewResultScreen
from screens.resultScreen import ResultScreen
from screens.parameterSelectionScreen import ParameterSelectionScreen
from screens.resultSelectionScreen import ResultSelectionScreen
from screens.parameterInTimeScreen import ParameterInTimeScreen
from screens.dataReferenceScreen import DataReferenceScreen


class AppScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.exam_id = None
        self.add_widget(LoginScreen(name="login"))
        self.add_widget(RegistrationScreen(name="registration"))
        self.add_widget(MainScreen(name="main"))
        self.add_widget(InfoScreen(name="info"))
        self.add_widget(ResultsScreen(name="results"))
        self.add_widget(NewResultScreen(name="new_result"))
        self.add_widget(ResultScreen(name="result"))
        self.add_widget(ParameterSelectionScreen(name="parameter_selection"))
        self.add_widget(ResultSelectionScreen(name="result_selection"))
        self.add_widget(ParameterInTimeScreen(name="parameter_in_time"))
        self.add_widget(DataReferenceScreen(name="data_reference"))
