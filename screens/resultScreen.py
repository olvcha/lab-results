from kivy.uix.screenmanager import Screen
from plotWidget import PlotWidget


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super(ResultScreen, self).__init__(**kwargs)
        #
        # # Example values
        # your_value = 50  # Value for the column height
        # max_value = 100  # Height of the maximum line
        # min_value = 20   # Height of the minimum line
        #
        # # Create an instance of PlotWidget and add it to the screen
        # plot_widget = PlotWidget(your_value, max_value, min_value)
        # self.add_widget(plot_widget)  # Add the plot widget to the screen