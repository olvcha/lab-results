import os

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

from textReader import TextReader

from kivy.uix.screenmanager import ScreenManager, Screen
from screens.myScreenManager import MyScreenManager
from screens.loginScreen import LoginScreen
from screens.newResultScreen import NewResultScreen


class LabResultsApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.kvs = Builder.load_string(KV)
        self.file_popup = None
        self.selected_file_path = None
        self.selected_file_name = None

    # def build(self):
    #     screen = Screen()
    #     screen.add_widget(self.kvs)
    #     return screen

    def build(self):
        Builder.load_file('main.kv')  # Load the KV file
        sm = MyScreenManager()
        #sm.add_widget(LoginScreen(name='login_screen'))
        #sm.add_widget(NewResultScreen(name='new_result_screen'))
        return sm


if __name__ == '__main__':
    LabResultsApp().run()
