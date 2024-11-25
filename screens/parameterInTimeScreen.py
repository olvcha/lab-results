import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from implementation.plotGenerator import PlotGenerator
from databaseFiles.tables.examinationTable import ExaminationTable
from implementation.parameterChangeGenerator import ParameterChangeGenerator

Builder.load_file(os.path.join(os.path.dirname(__file__), 'parameter_in_time_screen.kv'))


class ParameterInTimeScreen(Screen):
    '''Handle parameter in time screen actions.'''

    def __init__(self, **kwargs):
        super(ParameterInTimeScreen, self).__init__(**kwargs)

    def on_enter(self):
        self.display_parameter_in_time()

    def display_parameter_in_time(self):
        '''Display parameter in time plot.'''
        # Reference the plot container
        plot_container = self.ids.plot_container

        # Clear any existing widgets
        plot_container.clear_widgets()

        parameter_change_plots = ParameterChangeGenerator()
        results = parameter_change_plots.generate_results()

        for result in results:
            param_name = result["param_name"]
            plot_widget = result["plot_widget"]

            result_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=150,  # Set a fixed height for all rows
                padding=[10, 10],  # Add spacing around the entire layout
                spacing=10  # Space between left and right sides
            )

            plot_layout = GridLayout(
                cols=1,
                size_hint_x=0.6,
                size_hint_y=None,
                row_force_default=True,
                row_default_height=40,  # Match row height to the left side
                padding=[0, 10, 0, 10]  # Optional: Vertical padding for alignment
            )
            plot_layout.add_widget(
                Label(text=param_name, color=[0, 0, 0, 1], size_hint_y=None, height=30))
            plot_layout.add_widget(plot_widget)
            result_layout.add_widget(plot_layout)

            plot_container.add_widget(result_layout)

    def switch_to_result_screen(self):
        self.manager.current = 'result'

    def switch_to_data_reference_screen(self):
        self.manager.current = 'data_reference'

    def switch_to_result_selection_screen(self):
        self.manager.current = 'result_selection'
