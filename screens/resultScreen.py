import os
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel

from implementation.globalData import GlobalData
from implementation.plotGenerator import PlotGenerator
from databaseFiles.tables.examinationTable import ExaminationTable

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
        exam_id = self.global_data.get_exam_id()
        exam_data = self.exam_table.load_examination_data(exam_id)
        date = exam_data[1]

        # Reference the plot container
        plot_container = self.ids.plot_container
        plot_container.clear_widgets()

        labels_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=100,
            padding=[0, 0, 10, 0],
            spacing=5
        )

        # First label
        labels_layout.add_widget(
            Label(
                text="Oto twoje wyniki.",
                font_size='20sp',
                bold=True,
                size_hint_y=None,
                height=40,
                color=[0, 0, 0, 1],
                halign="left",
                valign="middle"
            )
        )

        # Second label
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

        plot_container.add_widget(labels_layout)
        plot_container.add_widget(
            BoxLayout(
                size_hint_y=None,
                height=20
            )
        )

        # Generate results using PlotGenerator
        plot_generator = PlotGenerator(str(exam_id))
        results = plot_generator.generate_results()

        for result in results:
            parameter_name = result["parameter_name"]
            loinc_code = result["loinc_code"]
            min_value = result["min_value"]
            max_value = result["max_value"]
            value = result["value"]
            unit = result["unit"]
            plot_widget = result["plot_widget"]

            result_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=150,  # Set a fixed height for all rows
                padding=[5, 5],
                spacing=15
            )

            # LEFT SIDE
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

            # RIGHT SIDE
            plot_with_label_layout = GridLayout(
                cols=1,
                size_hint_x=0.5,
                size_hint_y=None,
                row_force_default=True,
                row_default_height=40,
                padding=[0, 10, 0, 10]
            )

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

            plot_with_label_layout.add_widget(plot_widget)

            result_layout.add_widget(labels_layout)
            result_layout.add_widget(plot_with_label_layout)

            plot_container.add_widget(result_layout)

    def define_reference_value(self, min_value, max_value, value, unit):
        '''Get reference value (optionally with an indicator).'''
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
