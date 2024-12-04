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

        # Set padding and spacing for the plot container
        plot_container.padding = [10, 10, 10, 10]  # Apply consistent padding for the container

        parameter_change_plots = ParameterChangeGenerator()
        results = parameter_change_plots.generate_results()

        for result in results:
            #param_name = result["param_name"]
            plot_widget = result["plot_widget"]

            # Create a layout for each parameter plot
            plot_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,  # Let the height be manually controlled
                height=350,  # Set height to include label (30) + plot (300) + spacing
                spacing=10,  # Add spacing between label and plot
                padding=[10, 10, 10, 10]  # Padding inside this layout
            )

            # Add the parameter name label
            # plot_layout.add_widget(
            #     Label(text=param_name, color=[0, 0, 0, 1], size_hint_y=None, height=30)
            # )

            # Configure the plot widget
            plot_widget.size_hint_y = None
            plot_widget.height = 300
            plot_layout.add_widget(plot_widget)

            # Add the plot layout to the main container
            plot_container.add_widget(plot_layout)

    def switch_to_result_screen(self):
        self.manager.current = 'result'

    def switch_to_data_reference_screen(self):
        self.manager.current = 'data_reference'

    def switch_to_result_selection_screen(self):
        self.manager.current = 'result_selection'
