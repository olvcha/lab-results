import os
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from implementation.plotGenerator import PlotGenerator

Builder.load_file(os.path.join(os.path.dirname(__file__), 'result_screen.kv'))


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)

    def on_enter(self):
        # Get the exam_id from the app screen manager
        app_screen_manager = self.manager
        exam_id = app_screen_manager.get_exam_id()

        # Reference the plot container
        plot_container = self.ids.plot_container

        # Clear any existing widgets from the container before adding new ones
        plot_container.clear_widgets()

        # Generate plots using PlotGenerator
        plot_generator = PlotGenerator(str(exam_id))
        plot_widgets = plot_generator.generate_plots()

        # Add each plot widget to the plot_container
        for plot_widget in plot_widgets:
            plot_container.add_widget(plot_widget)

    def switch_to_main_screen(self):
        self.manager.current = 'main'
