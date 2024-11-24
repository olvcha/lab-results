import os

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from databaseFiles.tables.examinationTable import ExaminationTable
from implementation.fileManager import FileManager

Builder.load_file(os.path.join(os.path.dirname(__file__), 'data_reference_screen.kv'))


class DataReferenceScreen(Screen):
    def __init__(self, **kwargs):
        super(DataReferenceScreen, self).__init__(**kwargs)
        #self.exam_id = self.manager.get_exam_id()
        self.exam_table = ExaminationTable()
        self.file_manager = FileManager()

        self.display_data_reference()

    def on_enter(self):
        self.exam_id = self.manager.get_exam_id()
        exam_data = self.exam_table.load_examination_data(self.exam_id)
        data_reference = exam_data[2]

        image_widget = self.file_manager.display_image(data_reference)

        self.ids.image_container.clear_widgets()
        self.ids.image_container.add_widget(image_widget)
    def display_data_reference(self):
        '''Displays data reference image.'''
        #exam_id = self.manager.get_exam_id()
        # db = ExaminationTable()
        # file_manager = FileManager()


    def switch_to_result_screen(self):
        self.manager.current = 'result'
