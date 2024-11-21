import json
from time import sleep

from kivy_garden.matplotlib import FigureCanvasKivyAgg
from matplotlib import pyplot as plt
import matplotlib
from rapidfuzz import process

# matplotlib.use('Agg')  # Use 'Agg' for non-interactive plotting
from databaseFiles.tables.examinationTable import ExaminationTable

from implementation.dataExtraction import DataExtraction


class PlotGenerator:
    '''Responsible for processing raw data into visualisations in the form of plot'''

    def __init__(self, exam_id):
        self.examination_table = ExaminationTable()
        self.exam_data = self.examination_table.load_examination_data(str(exam_id))
        if not self.exam_data or not self.exam_data[0]:
            print(f"No data found for exam_id: {exam_id}")
            self.data = {}
        else:
            json_str = self.exam_data[3]
            self.exam_data = json.loads(json_str)

        if self.exam_data:
            self.data_extraction = DataExtraction(self.exam_data)
            self.filtered_exam_data = self.data_extraction.get_filtered_exam_data()
            self.parameters_data = self.data_extraction.get_parameters_data()
        else:
            self.filtered_exam_data = {}
            self.parameters_data = []

    ### shit here we go again
    def plot_parameter(self, param_name, min_value, ref_value, max_value, loinc_code):
        """
        Generates a horizontal bar plot with three colored segments:
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

        # Create the figure and axis with further reduced size (scaled by 0.5x again)
        fig, ax = plt.subplots(figsize=(0.5, 0.5))  # Scaling down the figure size by another half (0.25 total)

        red_color = (224 / 255, 122 / 255, 116 / 255)  # RGB red
        green_color = (155 / 255, 200 / 255, 122 / 255)  # RGB green
        yellow_color = (234 / 255, 208 / 255, 111 / 225)  # RGB yellow

        # Set smaller bar height and marker height (scaled down by another 0.5x)
        bar_height = 0.025  # Even thinner bar
        marker_height = 0.05  # Even shorter marker height

        # Plot the bar segments with further reduced height
        ax.barh([''], [2 * offset / 3], left=bar_start, color=red_color, height=bar_height, align='center')
        ax.barh([''], [offset / 3], left=min_value - offset / 3, color=yellow_color, height=bar_height, align='center')
        ax.barh([''], [max_value - min_value], left=min_value, color=green_color, height=bar_height, align='center')
        ax.barh([''], [offset / 3], left=max_value, color=yellow_color, height=bar_height, align='center')
        ax.barh([''], [2 * offset / 3], left=max_value + offset / 3, color=red_color, height=bar_height, align='center')

        # Add thick black marker with horizontal caps for ref_value (scaled down by 0.5x again)
        cap_length = 0.025 * offset  # Shorter horizontal caps
        marker_y_shift = 0  # Keep the marker aligned with the bar

        ax.vlines(clamped_ref_value, -marker_height / 2, marker_height / 2, colors='black',
                  linewidth=4)  # Shorter black line
        ax.hlines([marker_y_shift - marker_height / 2, marker_y_shift + marker_height / 2],
                  clamped_ref_value - cap_length, clamped_ref_value + cap_length, colors='black', linewidth=2)

        # Set labels and title with further reduced font size
        #ax.set_title(f'{param_name} (Loinc code: {loinc_code}) | Ref Value: {ref_value}',
        #             fontsize=5)  # Further scaled font size
        #ax.set_xlabel('Value', fontsize=5)  # Further scaled font size
        #ax.tick_params(axis='x', labelsize=5)  # Further scaled label size
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
        Generates a list of results, each containing:
        - param_name: Name of the parameter.
        - min_value, max_value, ref_value: Numeric values for the parameter.
        - loinc_code: Parameter code.
        - plot_widget: The plot widget for visualization.
        """
        results = []
        for _, param_name, min_value, max_value, loinc_code in self.parameters_data:
            # Match parameter name to its reference value
            ref_name = self.find_a_match(self.filtered_exam_data, param_name)
            ref_value = float(self.filtered_exam_data.get(f"{ref_name}", "0"))

            # Generate the plot widget
            plot_widget = self.plot_parameter(param_name, min_value, ref_value, max_value, loinc_code)

            # Append the result as a dictionary
            results.append({
                "param_name": param_name,
                "min_value": min_value,
                "max_value": max_value,
                "ref_value": ref_value,
                "plot_widget": plot_widget
            })

        return results

    def find_a_match(self, ref_data, param_name):
        '''Finds the closest match between parameter name and reference from exam data'''
        closest_match = process.extractOne(param_name, ref_data.keys(), score_cutoff=50)

        return closest_match[0] if closest_match else None

