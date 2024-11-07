import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Line

class PlotWidget(BoxLayout):
    def __init__(self, your_value, max_value, min_value, **kwargs):
        super(PlotWidget, self).__init__(**kwargs)
        self.orientation = 'vertical'
    #
    #     # Define sizes for the plot area
    #     self.plot_height = 300  # Height of the plot area
    #     self.plot_width = 200    # Width of the plot area
    #
    #     # Add the plot area to the widget
    #     with self.canvas:
    #         # Draw the background rectangle (plot area)
    #         Color(1, 1, 1, 1)  # White background
    #         Rectangle(pos=(0, 0), size=(self.plot_width, self.plot_height))
    #
    #         # Draw the bar for your_value
    #         self.draw_value(your_value, max_value)
    #
    #         # Draw the horizontal lines for max_value and min_value
    #         self.draw_lines(max_value, min_value)
    #
    # def draw_value(self, your_value, max_value):
    #     # Normalize the your_value based on the max_value
    #     normalized_value = (your_value / max_value) * self.plot_height
    #
    #     with self.canvas:
    #         # Set color for the column (blue)
    #         Color(0, 0, 1, 1)  # Blue color
    #         # Draw the rectangle representing your_value
    #         Rectangle(pos=(self.plot_width / 2 - 20, 0), size=(40, normalized_value))
    #
    # def draw_lines(self, max_value, min_value):
    #     # Normalize the lines based on the max_value
    #     max_line_pos = (max_value / max_value) * self.plot_height
    #     min_line_pos = (min_value / max_value) * self.plot_height
    #
    #     with self.canvas:
    #         # Set color for the max_value line (green)
    #         Color(0, 1, 0, 1)  # Green color
    #         Line(points=[0, max_line_pos, self.plot_width, max_line_pos], width=2)
    #
    #         # Set color for the min_value line (red)
    #         Color(1, 0, 0, 1)  # Red color
    #         Line(points=[0, min_line_pos, self.plot_width, min_line_pos], width=2)
