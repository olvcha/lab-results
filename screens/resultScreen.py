import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.label import MDIcon, MDLabel

from implementation.globalData import GlobalData
from implementation.plotGenerator import PlotGenerator
from databaseFiles.tables.examinationTable import ExaminationTable
from implementation.fileManager import FileManager

Builder.load_file(os.path.join(os.path.dirname(__file__), 'result_screen.kv'))


class ResultScreen(Screen):
    '''Handle result screen actions.'''

    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        self.exam_table = ExaminationTable()
        self.global_data = GlobalData()
        self.text_color = None

    def on_enter(self):
        self.display_result()

    def display_result(self):
        # exam_id = self.manager.get_exam_id()
        # global_data = GlobalData()
        exam_id = self.global_data.get_exam_id()

        # db = ExaminationTable()
        # file_manager = FileManager()
        exam_data = self.exam_table.load_examination_data(exam_id)
        date = exam_data[1]
        # data_reference = exam_data[2]

        # Reference the plot container
        plot_container = self.ids.plot_container

        # Clear any existing widgets
        plot_container.clear_widgets()

        # Container for the top-right-aligned labels
        labels_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=100,  # Adjust to fit the labels
            padding=[0, 0, 10, 0],  # Add right padding for alignment
            spacing=5
        )

        # Add the first label (right-aligned)
        labels_layout.add_widget(
            Label(
                text="Oto twoje wyniki.",
                font_size='20sp',
                bold=True,
                size_hint_y=None,
                height=40,
                color=[0, 0, 0, 1],  # Black color
                halign="left",
                valign="middle"
            )
        )

        # Add the second label (right-aligned)
        labels_layout.add_widget(
            Label(
                text=f"Data: {date}",
                font_size='16sp',
                size_hint_y=None,
                height=30,
                color=[0, 0, 0, 1],
                halign="left",
                valign="middle"
            )
        )

        # Add the labels layout to the plot container
        plot_container.add_widget(labels_layout)

        # Add a spacer to create space between the labels and results
        plot_container.add_widget(
            BoxLayout(
                size_hint_y=None,
                height=20  # Adjust the height to control spacing
            )
        )

        # Generate results using PlotGenerator
        plot_generator = PlotGenerator(str(exam_id))
        results = plot_generator.generate_results()

        # Dynamically add widgets for each result
        # Dynamically add widgets for each result
        # Dynamically add widgets for each result
        for result in results:
            parameter_name = result["parameter_name"]
            loinc_code = result["loinc_code"]
            min_value = result["min_value"]
            max_value = result["max_value"]
            value = result["value"]
            unit = result["unit"]
            plot_widget = result["plot_widget"]

            # Create a horizontal layout for the result with spacing
            result_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=150,  # Set a fixed height for all rows
                padding=[5, 5],
                spacing=15
            )

            # LEFT SIDE: Vertical layout for parameter information
            labels_layout = GridLayout(
                cols=1,
                size_hint_x=0.4,
                size_hint_y=None,
                row_force_default=True,
                row_default_height=40,
                padding=[0, 10, 0, 10]
            )
            labels_layout.add_widget(MDLabel(
                text=f"[b]{parameter_name}[/b]",
                markup=True,
                color=[0, 0, 0, 1],
                font_style="Title",
                role="medium",
                halign="center",
                valign="middle"
            ))
            labels_layout.add_widget(MDLabel(
                text=f"Kod LOINC: {loinc_code}",
                markup=True,
                color=[0, 0, 0, 1],
                font_style="Body",
                role="medium",
                halign="center",
                valign="middle"
            ))
            labels_layout.add_widget(MDLabel(
                text=f"Norma: {min_value} - {max_value} [{unit}]",
                color=[0, 0, 0, 1],
                font_style="Body",
                role="medium",
                halign="center",
                valign="middle"
            ))

            # RIGHT SIDE: Vertical layout for reference value, plot, and MDIcon
            plot_with_label_layout = GridLayout(
                cols=1,
                size_hint_x=0.5,
                size_hint_y=None,
                row_force_default=True,
                row_default_height=40,
                padding=[0, 10, 0, 10]
            )

            # Add the reference value to the layout
            plot_with_label_layout.add_widget(
                Label(
                    text=self.define_reference_value(min_value, max_value, value, unit),
                    markup=True,
                    font_name="Roboto",
                    color=self.text_color,
                    size_hint_y=None,
                    height=30
                )
            )

            # Add the plot_widget
            plot_with_label_layout.add_widget(plot_widget)

            # Add the MDIcon vertically centered
            md_icon = MDIcon(
                id='date_icon',
                icon='emoticon',
                size_hint_y=None,
                halign="center",
                height=30,
                # pos_hint={"center_y": 0.5}  # Center the icon vertically
            )
            # plot_with_label_layout.add_widget(md_icon)

            # Combine the left and right layouts into the horizontal result layout
            result_layout.add_widget(labels_layout)
            result_layout.add_widget(plot_with_label_layout)

            # Add the entire result layout to the main scrollable container
            plot_container.add_widget(result_layout)

    def define_reference_value(self, min_value, max_value, value, unit):
        if float(value) < float(min_value):
            self.text_color = [1, 0, 0, 1]
            return f"[b]{value}[/b] [{unit}]  [b]v[/b]"
        elif float(value) > float(max_value):
            self.text_color = [1, 0, 0, 1]
            return f"[b]{value}[/b] [{unit}]  [b]^[/b]"
        self.text_color = [0, 0, 0, 1]
        return f"[b]{value}[/b] [{unit}]"



    def switch_to_main_screen(self):
        self.manager.current = 'main'

    def switch_to_parameter_in_time_screen(self):
        self.manager.current = 'parameter_in_time'

    def switch_to_data_reference_screen(self):
        self.manager.current = 'data_reference'

    def switch_to_results_screen(self):
        self.manager.current = 'results'
