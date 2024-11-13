import os

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from implementation.plotGenerator import PlotGenerator

Builder.load_file(os.path.join(os.path.dirname(__file__), 'result_screen.kv'))


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        #plot_generator = PlotGenerator(exam_data)
        #print(exam_data)
        # self.exam_id = None
        # self.on_enter()
        self.exam_id_label = Label()
        self.add_widget(self.exam_id_label)
        self.layout = BoxLayout(orientation='vertical')



    def on_enter(self):
        # Access the exam_id from the AppScreenManager
        app_screen_manager = self.manager
        exam_id = app_screen_manager.get_exam_id()

        # Update the label with the exam_id
        self.exam_id_label.text = f"Exam ID: {exam_id}"
        self.exam_id = exam_id

        self.plot_generator = PlotGenerator(str(exam_id))
        #self.plot_generator = PlotGenerator(str(1))

        plot_widgets = self.plot_generator.generate_plots()

        # Add the generated plot widgets to the layout
        for plot_widget in plot_widgets:
            self.layout.add_widget(plot_widget)

        # Add the layout to the screen
        self.add_widget(self.layout)


