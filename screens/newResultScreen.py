from datetime import datetime, date
import os

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, \
    MDDialogButtonContainer
from kivymd.uix.pickers import MDModalDatePicker

from databaseFiles.tables.examinationTable import ExaminationTable
from databaseFiles.tables.examinationParameterTable import ExaminationParameterTable
from databaseFiles.tables.parameterTable import ParameterTable

from implementation.globalData import GlobalData
from implementation.textReader import TextReader
from implementation.fileManager import FileManager
from implementation.dataExtraction import DataExtraction
from implementation.pdfTextReader import PdfTextReader

Builder.load_file(os.path.join(os.path.dirname(__file__), 'new_result_screen.kv'))


class NewResultScreen(Screen):
    '''Handle new result screen actions'''

    def __init__(self, **kwargs):
        super(NewResultScreen, self).__init__(**kwargs)
        self.exam_id = None
        self.file_popup = None
        self.selected_file_path = None
        self.selected_file_name = None
        self.date_dialog = None
        self.selected_date = None
        self.error_dialog = None
        self.examination_table = ExaminationTable()
        self.file_manager = FileManager()
        self.global_data = GlobalData()
        self.examination_parameter_table = ExaminationParameterTable()
        self.parameter_table = ParameterTable()

    def on_enter(self):
        # File
        self.ids.load_button_text.text = "Wybierz plik"
        self.ids.file_icon.icon = 'close'
        self.ids.load_button.disabled = True
        # Date
        self.ids.date_button_text.text = "Wybierz datę"
        self.ids.date_icon.icon = 'close'
        # Analize
        self.ids.data_button.disabled = True

    def load_data(self):
        '''Pop-up window for file selection and loading.'''
        content = BoxLayout(orientation='vertical')

        filechooser = FileChooserListView(filters=['*.pdf', '*.png', '*.jpg', '*.jpeg', '*.gif'])
        content.add_widget(filechooser)

        select_button = Button(text="Wybierz", size_hint_y=None, height=40)
        select_button.bind(on_release=lambda x: self.select_file(filechooser.selection))
        content.add_widget(select_button)

        self.file_popup = Popup(title="Wybierz plik",
                                content=content,
                                size_hint=(0.9, 0.9))
        self.file_popup.open()

    def select_file(self, selection):
        '''Show file selection.'''
        if selection:
            self.selected_file_path = selection[0]
            self.selected_file_name = os.path.basename(self.selected_file_path)
            self.ids.load_button_text.text = self.selected_file_name
            self.ids.file_icon.icon = 'check'
            self.convert_data()

        self.file_popup.dismiss()

    def convert_data(self):
        '''Convert the given data.'''
        file_extension = os.path.splitext(self.selected_file_path)[1].lower()

        if file_extension == '.pdf':
            pdf_reader = PdfTextReader(self.selected_file_path)
            json_text = pdf_reader.save_to_json()
        elif file_extension in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            text_reader = TextReader(self.selected_file_path)
            text_reader.read_text()
            json_text = text_reader.save_to_json()
        else:
            json_text = {}

        filtered_parameters_data = self.extract_parameters_data(json_text)
        self.check_data(json_text, filtered_parameters_data)

    def extract_parameters_data(self, exam_data):
        '''Extract and filter parameters data and leave only the parameters that appear in the database.'''
        data_extraction = DataExtraction(exam_data)
        filtered_exam_data = data_extraction.filter_exam_data()

        return filtered_exam_data

    def save_parameters_data(self, exam_id, filtered_exam_data):
        '''Save examination parameters to the database.'''
        for parameter_id, value in filtered_exam_data.items():
            priority_id = self.parameter_table.get_priority_parameter(parameter_id)[0]
            self.examination_parameter_table.add_examination_parameter(value, exam_id, priority_id)

    def extract_and_save(self, exam_data, exam_id):
        '''Extract the parameters data and save to the database.'''
        data_extraction = DataExtraction(exam_data)
        filtered_exam_data = data_extraction.filter_exam_data()
        for parameter_id, value in filtered_exam_data.items():
            self.examination_parameter_table.add_examination_parameter(value, exam_id, parameter_id)

    def show_date_picker(self):
        '''Show the date picker.'''
        self.date_dialog = MDModalDatePicker()
        self.date_dialog.bind(on_ok=self.on_save, on_cancel=self.on_cancel)
        self.date_dialog.open()

    def on_cancel(self, instance):
        '''Cancel the date picker.'''
        self.date_dialog.dismiss()

    def on_save(self, instance):
        '''Save selected date and cancel the date picker'''
        self.selected_date = instance.get_date()[0].strftime('%d-%m-%Y')
        if instance.get_date()[0] <= date.today():
            self.ids.date_icon.icon = 'check'
            self.ids.date_button_text.text = str(self.selected_date)
            self.ids.load_button.disabled = False
            self.date_dialog.dismiss()
        else:
            self.ids.date_button_text.text = "Niepoprawna data."
            self.ids.date_icon.icon = 'close'
            self.ids.load_button.disabled = True
            self.date_dialog.dismiss()

    def check_data(self, data, filtered_data):
        '''Check if read data is valid. Save data to database if True, else raise an error.'''
        if not filtered_data:
            self.show_info_dialog()
        else:
            user_id = self.global_data.get_user_id()
            file_id = self.file_manager.upload_file(self.selected_file_path, user_id, self.selected_date)

            self.exam_id = self.examination_table.add_examination(user_id, self.selected_date,
                                                                  file_id, data)

            self.save_parameters_data(self.exam_id, filtered_data)
            #self.extract_and_save(data, self.exam_id)
            self.ids.data_button.disabled = False

    def show_info_dialog(self):
        self.error_dialog = MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="information",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="Informacja",
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text="Błąd przetwarzania. Przesłano plik w złym formacie lub nie wykryto parametrów. Spróbuj ponownie.",
                halign="left",
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Zamknij"),
                    style="text",
                    on_release=lambda *args: self.error_dialog.dismiss()
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
        )
        self.error_dialog.open()

    def switch_to_main_screen(self):
        self.manager.current = 'main'

    def switch_to_result_screen(self):
        app_screen_manager = self.manager
        # app_screen_manager.set_exam_id(str(self.exam_id))
        global_data = GlobalData()
        global_data.set_exam_id(str(self.exam_id))
        self.manager.current = 'result'
