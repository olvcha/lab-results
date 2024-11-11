import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from databaseFiles.tables.examinationTable import ExaminationTable

Builder.load_file(os.path.join(os.path.dirname(__file__), 'result_selection_screen.kv'))


class ResultSelectionScreen(Screen):
    '''Handles result screen actions'''
    def __init__(self, **kwargs):
        super(ResultSelectionScreen, self).__init__(**kwargs)
        self.examinationTable = ExaminationTable()

    def switch_to_results_screen(self):
        '''Switches to the results screen'''
        self.manager.current = 'results'

    def load_buttons(self):
        '''Load the buttons. The number of buttons depends on the amount of data in the database, it is flexible.'''
        button_container = self.ids.button_container
        button_container.clear_widgets()

        app = MDApp.get_running_app()
        user_id = app.get_user_id()

        examination_tuple = self.examinationTable.fetch_examination_data(user_id)

        for record in examination_tuple:
            button = MDButton(
                style="filled",
                theme_width="Custom",
                pos_hint={'center_x': 0.5},
                height="56dp",
                size_hint_x=0.8,
                on_release=lambda btn, record_name=record: self.on_button_press(record_name)
            )
            button_text = MDButtonText(
                text=record[1],
                pos_hint={'center_x': 0.5, 'center_y': 0.5}
            )
            button.add_widget(button_text)
            button_container.add_widget(button)

    def on_button_press(self, record_name):
        print(f"Button for {record_name} pressed")
