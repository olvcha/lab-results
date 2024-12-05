import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from databaseFiles.tables.examinationTable import ExaminationTable
from implementation.fileManager import FileManager
from implementation.globalData import GlobalData

Builder.load_file(os.path.join(os.path.dirname(__file__), 'data_reference_screen.kv'))


class DataReferenceScreen(Screen):
    '''Handles data reference screen actions'''
    def __init__(self, **kwargs):
        super(DataReferenceScreen, self).__init__(**kwargs)
        # self.exam_id = self.manager.get_exam_id()
        self.exam_table = ExaminationTable()
        self.file_manager = FileManager()
        self.global_data = GlobalData()

    def on_enter(self):
        self.display_data_reference()

    def display_data_reference(self):
        '''Display data reference (images or PDFs).'''
        exam_id = self.global_data.get_exam_id()
        exam_data = self.exam_table.load_examination_data(exam_id)
        data_reference = exam_data[2]

        file_widgets = self.file_manager.display_file(data_reference)

        self.ids.image_container.clear_widgets()

        for widget in file_widgets:
            self.ids.image_container.add_widget(widget)

    def switch_to_result_screen(self):
        self.manager.current = 'result'

    def switch_to_parameter_in_time_screen(self):
        self.manager.current = 'parameter_in_time'

    def switch_to_results_screen(self):
        self.manager.current = 'results'
