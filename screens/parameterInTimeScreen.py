import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogSupportingText, \
    MDDialogButtonContainer

from implementation.plotGenerator import PlotGenerator
from databaseFiles.tables.examinationTable import ExaminationTable
from implementation.parameterChangeGenerator import ParameterChangeGenerator

Builder.load_file(os.path.join(os.path.dirname(__file__), 'parameter_in_time_screen.kv'))


class ParameterInTimeScreen(Screen):
    '''Handle parameter in time screen actions.'''

    def __init__(self, **kwargs):
        super(ParameterInTimeScreen, self).__init__(**kwargs)
        self.info_dialog = None

    def on_enter(self):
        self.display_parameter_in_time()

    def display_parameter_in_time(self):
        '''Display parameter in time plot.'''
        plot_container = self.ids.plot_container
        plot_container.clear_widgets()
        plot_container.padding = [10, 10, 10, 10]

        parameter_change_plots = ParameterChangeGenerator()
        results = parameter_change_plots.generate_results()

        if len(results) > 0:
            for result in results:
                plot_widget = result["plot_widget"]
                plot_layout = BoxLayout(
                    orientation='vertical',
                    size_hint_y=None,
                    height=350,
                    spacing=10,
                    padding=[10, 10, 10, 10]
                )

                # Configuration
                plot_widget.size_hint_y = None
                plot_widget.height = 300
                plot_layout.add_widget(plot_widget)

                # Add to the main container
                plot_container.add_widget(plot_layout)
        else:
            self.show_info_dialog()

    def show_info_dialog(self):
        self.info_dialog = MDDialog(
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
                text="Niewystarczająca ilość danych. Dodaj kolejne wyniki, aby uzyskać dostęp do porównania.",
                halign="left",
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Zamknij"),
                    style="text",
                    on_release=lambda *args: self.info_dialog_action()
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
        )
        self.info_dialog.open()

    def info_dialog_action(self):
        self.switch_to_result_screen()
        self.info_dialog.dismiss()

    def switch_to_result_screen(self):
        self.manager.current = 'result'

    def switch_to_data_reference_screen(self):
        self.manager.current = 'data_reference'

    def switch_to_results_screen(self):
        self.manager.current = 'results'
