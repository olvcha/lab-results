import os
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from implementation.plotGenerator import PlotGenerator
from databaseFiles.tables.examinationTable import ExaminationTable
from implementation.fileManager import FileManager

Builder.load_file(os.path.join(os.path.dirname(__file__), 'result_screen.kv'))


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)

    def on_enter(self):
        #self.update_button_colors(active_button=self.details_button)
        # Get the exam_id from the app screen manager
        exam_id = self.manager.get_exam_id()
        db = ExaminationTable()
        file_manager = FileManager()
        exam_data = db.load_examination_data(exam_id)
        date = exam_data[1]
        data_reference = exam_data[2]

        #image_widget = file_manager.display_image(data_reference)
        # Clear existing widgets (optional)
        #self.ids.image_container.clear_widgets()

        # Add the image widget to the layout container
        #self.ids.image_container.add_widget(image_widget)

        # Reference the plot container
        plot_container = self.ids.plot_container

        # Clear any existing widgets
        plot_container.clear_widgets()

        # Container for the top-right-aligned labels
        labels_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=80,  # Adjust to fit the labels
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
        for result in results:
            param_name = result["param_name"]
            min_value = result["min_value"]
            max_value = result["max_value"]
            ref_value = result["ref_value"]
            plot_widget = result["plot_widget"]

            # Create a horizontal layout for the result with spacing
            result_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=150,  # Set a fixed height for all rows
                padding=[10, 10],  # Add spacing around the entire layout
                spacing=10  # Space between left and right sides
            )

            # LEFT SIDE: Vertical layout for parameter information
            labels_layout = GridLayout(
                cols=1,
                size_hint_x=0.4,
                size_hint_y=None,
                row_force_default=True,
                row_default_height=40,  # Consistent row height for alignment
                padding=[0, 10, 0, 10]  # Optional: Vertical padding for alignment
            )
            labels_layout.add_widget(Label(text=f"[b]{param_name}[/b]", markup=True, color=[0, 0, 0, 1]))
            labels_layout.add_widget(Label(text=f"Norma: {min_value} - {max_value}", color=[0, 0, 0, 1]))

            # RIGHT SIDE: Vertical layout for reference value and plot
            plot_with_label_layout = GridLayout(
                cols=1,
                size_hint_x=0.6,
                size_hint_y=None,
                row_force_default=True,
                row_default_height=40,  # Match row height to the left side
                padding=[0, 10, 0, 10]  # Optional: Vertical padding for alignment
            )
            plot_with_label_layout.add_widget(
                Label(text=f"Ref: {ref_value}", color=[0, 0, 0, 1], size_hint_y=None, height=30))
            plot_with_label_layout.add_widget(plot_widget)

            # Add both layouts to the result layout
            result_layout.add_widget(labels_layout)
            result_layout.add_widget(plot_with_label_layout)

            # Add the result layout to the plot container
            plot_container.add_widget(result_layout)

    def switch_to_main_screen(self):
        self.manager.current = 'main'

    def switch_to_parameter_in_time_screen(self):
        self.manager.current = 'parameter_in_time'

    def switch_to_data_reference_screen(self):
        self.manager.current = 'data_reference'

    def toggle_button_colors(self, active_button):
        # Update the button colors dynamically based on the pressed button
        self.update_button_colors(active_button=active_button)

    def update_button_colors(self, active_button):
        # Define colors for the active and inactive buttons
        active_color = [0.4, 0, 0.6, 1]  # Dark violet
        inactive_color = [0.7, 0.6, 0.8, 1]  # Light violet

        # Apply colors
        if active_button == self.details_button:
            self.details_button.md_bg_color = active_color
            self.parameter_in_time_button.md_bg_color = inactive_color
        elif active_button == self.parameter_in_time_button:
            self.details_button.md_bg_color = inactive_color
            self.parameter_in_time_button.md_bg_color = active_color

    def parameter_in_time_button_action(self):
        self.manager.current = 'parameter_in_time'




