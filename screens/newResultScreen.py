import os

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from databaseFiles.tables.examinationTable import ExaminationTable
from datetime import datetime

from textReader import TextReader

Builder.load_file(os.path.join(os.path.dirname(__file__), 'new_result_screen.kv'))


class NewResultScreen(Screen):

    def __init__(self, **kwargs):
        super(NewResultScreen, self).__init__(**kwargs)

        self.file_popup = None
        self.selected_file_path = None
        self.selected_file_name = None
        self.examination_table = ExaminationTable()

    def switch_to_main_screen(self):
        self.manager.current = 'main'

    def load_data(self):
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
        text_reader = TextReader(self.selected_file_path)
        text_reader.read_text()
        text_reader.save_to_json('data.json')
        self.examination_table.add_examination(1, datetime.now(), self.selected_file_name, 'to wynik')
