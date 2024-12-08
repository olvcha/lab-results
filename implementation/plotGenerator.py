from kivy_garden.matplotlib import FigureCanvasKivyAgg
from matplotlib import pyplot as plt

from databaseFiles.tables.examinationParameterTable import ExaminationParameterTable
from databaseFiles.tables.parameterTable import ParameterTable


class PlotGenerator:
    '''Responsible for processing raw data into visualisations in the form of plot'''

    def __init__(self, exam_id):
        self.examination_parameter_table = ExaminationParameterTable()
        self.parameter_table = ParameterTable()

        try:
            self.examination_parameters = self.examination_parameter_table.get_examination_parameters_by_exam_id(
                exam_id)
        except KeyError:
            print(f"Key error: No data found for exam_id: {exam_id}")
        except ValueError:
            print(f"Value error: Invalid data for exam_id: {exam_id}")

    def plot_parameter(self, min_value, ref_value, max_value):
        """
        Generate a horizontal bar plot with three colored segments:
        - The bar spans from (min_value - offset) to (max_value + offset).
        - Three colored segments: red, yellow, and green.
        """
        # Calculate range offset
        offset = max_value - min_value
        bar_start = min_value - offset
        bar_end = max_value + offset

        # Clamp ref_value to the range
        if ref_value < bar_start:
            clamped_ref_value = bar_start
        elif ref_value > bar_end:
            clamped_ref_value = bar_end
        else:
            clamped_ref_value = ref_value

        fig, ax = plt.subplots(figsize=(0.5, 0.5))

        red_color = (224 / 255, 122 / 255, 116 / 255)
        green_color = (155 / 255, 200 / 255, 122 / 255)
        yellow_color = (234 / 255, 208 / 255, 111 / 225)

        bar_height = 0.025
        marker_height = 0.05

        # Plot the bar segments
        ax.barh([''], [2 * offset / 3], left=bar_start, color=red_color, height=bar_height, align='center')
        ax.barh([''], [offset / 3], left=min_value - offset / 3, color=yellow_color, height=bar_height, align='center')
        ax.barh([''], [max_value - min_value], left=min_value, color=green_color, height=bar_height, align='center')
        ax.barh([''], [offset / 3], left=max_value, color=yellow_color, height=bar_height, align='center')
        ax.barh([''], [2 * offset / 3], left=max_value + offset / 3, color=red_color, height=bar_height, align='center')

        # Add thick black marker with horizontal caps for ref_value (scaled down by 0.5x again)
        cap_length = 0.025 * offset
        marker_y_shift = 0

        ax.vlines(clamped_ref_value, -marker_height / 2, marker_height / 2, colors='black',
                  linewidth=4)
        ax.hlines([marker_y_shift - marker_height / 2, marker_y_shift + marker_height / 2],
                  clamped_ref_value - cap_length, clamped_ref_value + cap_length, colors='black', linewidth=2)

        ax.axis('off')

        # Remove y-axis ticks and labels
        ax.set_yticks([])

        # Set x-axis limits for some padding around the bar
        ax.set_xlim(bar_start - 0.1 * offset, bar_end + 0.1 * offset)

        # Use tight layout to minimize white space
        plt.tight_layout()

        # Return the plot as a Kivy widget (FigureCanvasKivyAgg)
        return FigureCanvasKivyAgg(fig)

    def generate_results(self):
        """
        Generate a list of results, each containing:
        - param_name: Name of the parameter.
        - loinc_code: Parameter code.
        - min_value, max_value, value: Numeric values for the parameter.
        - plot_widget: The plot widget for visualization.
        """
        results = []
        for value, parameter_id in self.examination_parameters:
            parameter_data = self.parameter_table.load_parameter_data(parameter_id)
            parameter_name = parameter_data[0][1]
            min_value = parameter_data[0][2]
            max_value = parameter_data[0][3]
            unit = parameter_data[0][4]
            loinc_code = parameter_data[0][5]
            plot_widget = self.plot_parameter(float(min_value), float(value), float(max_value))

            results.append({
                "parameter_name": parameter_name,
                "loinc_code": loinc_code,
                "min_value": min_value,
                "max_value": max_value,
                "value": value,
                "unit": unit,
                "plot_widget": plot_widget
            })

        return results
