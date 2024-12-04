import os

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp

from databaseFiles.tables.examinationTable import ExaminationTable
from databaseFiles.tables.examinationParameterTable import ExaminationParameterTable
from datetime import datetime

from implementation.dataExtraction import DataExtraction
from implementation.globalData import GlobalData
from textReader import TextReader
from implementation.fileManager import FileManager
from implementation.dataExtractionN import DataExtractionN

Builder.load_file(os.path.join(os.path.dirname(__file__), 'new_result_screen.kv'))


class NewResultScreen(Screen):
    '''Handle new result screen actions'''

    def __init__(self, **kwargs):
        super(NewResultScreen, self).__init__(**kwargs)
        self.exam_id = None
        self.file_popup = None
        self.selected_file_path = None
        self.selected_file_name = None
        self.examination_table = ExaminationTable()
        self.file_manager = FileManager()
        self.global_data = GlobalData()
        self.examination_parameter_table = ExaminationParameterTable()

    def load_data(self):
        '''Pop-up window for file selection and loading.'''
        content = BoxLayout(orientation='vertical')

        filechooser = FileChooserListView(filters=['*.pdf', '*.png', '*.jpg', '*.jpeg', '*.gif'])
        content.add_widget(filechooser)

        select_button = Button(text="Select", size_hint_y=None, height=40)
        select_button.bind(on_release=lambda x: self.select_file(filechooser.selection))
        content.add_widget(select_button)

        self.file_popup = Popup(title="Select a File",
                                content=content,
                                size_hint=(0.9, 0.9))
        self.file_popup.open()

    def select_file(self, selection):
        '''Show file selection.'''
        if selection:
            self.selected_file_path = selection[0]
            self.selected_file_name = os.path.basename(self.selected_file_path)
            print(f"Selected file: {self.selected_file_path}")
            self.ids.file_path_label.text = f"Selected file: {self.selected_file_name}"
            self.ids.data_button.disabled = False
            self.convert_data()

        # Update the UI or handle the file path as needed
        self.file_popup.dismiss()

    def convert_data(self):
        '''Convert the given data.'''
        text_reader = TextReader(self.selected_file_path)
        text_reader.read_text()
        json_text = text_reader.save_to_json('data.json')

        # app = MDApp.get_running_app()
        # user_id = app.get_user_id()
        # global_data = GlobalData()
        user_id = self.global_data.get_user_id()

        # file_manager = FileManager()
        file_id = self.file_manager.upload_file(self.selected_file_path, user_id, datetime.now().strftime('%d-%m-%Y'))

        self.exam_id = self.examination_table.add_examination(user_id, datetime.now().strftime('%d-%m-%Y'),
                                                              file_id, json_text)

        self.extract_and_save(json_text, self.exam_id)

    def extract_and_save(self, exam_data, exam_id):
        '''Extract the parameters data and save to the database.'''
        data_extraction = DataExtractionN(exam_data)
        filtered_exam_data = data_extraction.filter_exam_data()
        for parameter_id, value in filtered_exam_data.items():
            self.examination_parameter_table.add_examination_parameter(value, exam_id, parameter_id)


    def switch_to_main_screen(self):
        self.manager.current = 'main'

    def switch_to_result_screen(self):
        app_screen_manager = self.manager
        # app_screen_manager.set_exam_id(str(self.exam_id))
        global_data = GlobalData()
        global_data.set_exam_id(str(self.exam_id))
        # app_screen_manager.set_exam_id("1")
        self.manager.current = 'result'
