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
            json_str = self.exam_data[0][0]
            self.exam_data = json.loads(json_str)

        if self.exam_data:
            self.data_extraction = DataExtraction(self.exam_data)
            self.filtered_exam_data = self.data_extraction.get_filtered_exam_data()
            self.parameters_data = self.data_extraction.get_parameters_data()
        else:
            self.filtered_exam_data = {}
            self.parameters_data = []

    # def plot_parameter(self, param_name, min_value, ref_value, max_value, loinc_code):
    #     '''Generates a bar plot and returns it as a FigureCanvasKivyAgg widget.'''
    #     fig, ax = plt.subplots(figsize=(6, 4))
    #     ax.bar(['Min Value', 'Ref Value', 'Max Value'], [min_value, ref_value, max_value],
    #            color=['skyblue', 'orange', 'lightgreen'])
    #     ax.set_title(f'{param_name} (Loinc code: {loinc_code})')
    #     ax.set_xlabel('Parameter')
    #     ax.set_ylabel('Value')
    #     ax.set_ylim(min(0, min_value - 1), max_value + 1)
    #
    #     # Return the plot as a Kivy widget (FigureCanvasKivyAgg)
    #     return FigureCanvasKivyAgg(fig)

    ### bez osi
    # def plot_parameter(self, param_name, min_value, ref_value, max_value, loinc_code):
    #     '''Generates a compact plot with just the bar and markers for min, ref, and max values.'''
    #
    #     # Create the figure with a compact size
    #     fig, ax = plt.subplots(figsize=(3, 2))  # Adjust the figure size to be compact
    #
    #     # Plot a single horizontal bar for the reference value
    #     ax.barh(['Ref Value'], [ref_value], color='orange', height=0.006)
    #
    #     # Add vertical dashed lines for min_value and max_value
    #     ax.vlines(min_value, -0.01, 0.01, colors='skyblue', linestyles='dashed', linewidth=2)
    #     ax.vlines(max_value, -0.01, 0.01, colors='lightgreen', linestyles='dashed', linewidth=2)
    #
    #     # Optional: Add scatter points for min_value and max_value for visibility
    #     #ax.scatter([min_value], [0], color='skyblue', s=60, zorder=5)
    #     #ax.scatter([max_value], [0], color='lightgreen', s=60, zorder=5)
    #
    #     # Annotate the values directly on the plot
    #     ax.text(ref_value, 0, f'Ref: {ref_value}', va='center', ha='left', color='black', fontsize=15)
    #     ax.text(min_value, 0, f'Min: {min_value}', va='center', ha='right', color='skyblue', fontsize=15)
    #     ax.text(max_value, 0, f'Max: {max_value}', va='center', ha='left', color='lightgreen', fontsize=15)
    #
    #     # Remove x and y axis labels and ticks
    #     ax.set_xticks([])  # No x-axis ticks
    #     ax.set_yticks([])  # No y-axis ticks
    #     ax.set_xticklabels([])  # No x-axis labels
    #     ax.set_yticklabels([])  # No y-axis labels
    #
    #     # Remove frame and grid
    #     ax.spines['top'].set_visible(False)
    #     ax.spines['right'].set_visible(False)
    #     ax.spines['left'].set_visible(False)
    #     ax.spines['bottom'].set_visible(False)
    #     ax.grid(False)  # No grid lines
    #
    #     # Set x-axis limits to ensure markers and values fit nicely within the plot
    #     ax.set_xlim(min(0, min_value - 1), max_value + 1)
    #
    #     # Return the plot as a Kivy widget (FigureCanvasKivyAgg)

    ### z osiami
    # def plot_parameter(self, param_name, min_value, ref_value, max_value, loinc_code):
    #     '''Generates a slim, vertical bar plot with markers for min_value and max_value along the ref_value bar.'''
    #
    #     # Make the figure even narrower
    #     fig, ax = plt.subplots(figsize=(2, 6))
    #
    #     # Plot a single horizontal bar for the reference value with a reduced height
    #     ax.barh(['Ref Value'], [ref_value], color='orange', height=0.2)  # Set height to 0.2 to make it slimmer
    #
    #     # Add vertical dashed lines for min_value and max_value
    #     ax.vlines(min_value, -0.1, 0.1, colors='skyblue', linestyles='dashed', linewidth=2, label='Min Value')
    #     ax.vlines(max_value, -0.1, 0.1, colors='lightgreen', linestyles='dashed', linewidth=2, label='Max Value')
    #
    #     # Set title and labels
    #     ax.set_title(f'{param_name} (Loinc code: {loinc_code})')
    #     ax.set_xlabel('Value')
    #     ax.set_ylim(-0.3, 0.3)  # Tight y-axis to fit around the slim bar
    #
    #     # Set x-axis limits to provide a small space around the min and max markers
    #     ax.set_xlim(min(0, min_value - 1), max_value + 1)
    #
    #     # Display a legend
    #     ax.legend(loc='best')
    #
    #     # Return the plot as a Kivy widget (FigureCanvasKivyAgg)
    #     return FigureCanvasKivyAgg(fig)

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

    ### same bary
    # def plot_parameter(self, param_name, min_value, ref_value, max_value, loinc_code):
    #     # Create a figure for each parameter
    #     fig, ax = plt.subplots(figsize=(6, 2))
    #     ax.barh([''], [ref_value], color='orange')
    #     ax.vlines([min_value, max_value], -0.5, 0.5, color=['blue', 'green'])
    #     ax.set_title(f'{param_name} (Loinc code: {loinc_code})')
    #     ax.set_yticks([])
    #     return FigureCanvasKivyAgg(fig)

    def generate_plots(self):
        '''Generates a list of plot widgets for each parameter in the parameters_data.'''
        plot_widgets = []
        for _, param_name, min_value, max_value, loinc_code in self.parameters_data:
            # Look for the reference value in the filtered_exam_data
            ref_name = self.find_a_match(self.filtered_exam_data, param_name)
            ref_value = float(self.filtered_exam_data.get(f"{ref_name}", "0"))

            # Generate the plot widget and add it to the list
            plot_widget = self.plot_parameter(param_name, min_value, ref_value, max_value, loinc_code)
            plot_widgets.append(plot_widget)

        return plot_widgets

    def find_a_match(self, ref_data, param_name):
        '''Finds the closest match between parameter name and reference from exam data'''
        closest_match = process.extractOne(param_name, ref_data.keys(), score_cutoff=50)

        return closest_match[0] if closest_match else None

