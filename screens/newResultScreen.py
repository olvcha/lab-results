import os

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from databaseFiles.tables.examinationTable import ExaminationTable

from textReader import TextReader

# KV = '''
# MDScreen:
#     md_bg_color: app.theme_cls.surfaceColor
#
#     AnchorLayout:
#         anchor_x: 'center'
#         anchor_y: 'top'
#         MDTopAppBar:
#             title: "Lab Results"
#     MDButton:
#         id: load_button
#         style: "elevated"
#         pos_hint: {'center_x':0.5, 'center_y':0.6}
#         on_release: root.load_data()
#
#         MDButtonIcon:
#             icon: "plus"
#
#         MDButtonText:
#             text: "Load PDF"
#
#     MDLabel:
#         id: file_path_label
#         text: "No file selected"
#         halign: "center"
#         pos_hint: {'center_x':0.5, 'center_y':0.5}
#
#     MDButton:
#         id: data_button
#         style: "elevated"
#         pos_hint: {'center_x':0.5, 'center_y':0.2}
#         disabled: True
#         on_release: app.convert_data()
#
#         MDButtonText:
#             text: "View Results"
#
# '''


class NewResultScreen(Screen):


    def __init__(self, **kwargs):
        super(NewResultScreen, self).__init__(**kwargs)
        #self.kvs = Builder.load_string(KV)
        #layout = BoxLayout(orientation='vertical')
        #layout.add_widget(self.kvs)
        #layout.add_widget(Button(text='Go to Login Screen', on_press=self.switch_to_login_screen))
        #self.add_widget(layout)

        self.file_popup = None
        self.selected_file_path = None
        self.selected_file_name = None
        self.examination_table = ExaminationTable()

    def switch_to_login_screen(self, instance):
        self.manager.current = 'login_screen'

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
        self.examination_table.add_examination(1, self.selected_file_name, 'to wynik')


