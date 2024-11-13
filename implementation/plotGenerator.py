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

    def plot_parameter(self, param_name, min_value, ref_value, max_value, loinc_code):
        '''Generates a compact plot with just the bar and markers for min, ref, and max values.'''

        # Create the figure with a compact size
        fig, ax = plt.subplots(figsize=(3, 2))  # Adjust the figure size to be compact

        # Plot a single horizontal bar for the reference value
        ax.barh(['Ref Value'], [ref_value], color='orange', height=0.006)

        # Add vertical dashed lines for min_value and max_value
        ax.vlines(min_value, -0.01, 0.01, colors='skyblue', linestyles='dashed', linewidth=2)
        ax.vlines(max_value, -0.01, 0.01, colors='lightgreen', linestyles='dashed', linewidth=2)

        # Optional: Add scatter points for min_value and max_value for visibility
        #ax.scatter([min_value], [0], color='skyblue', s=60, zorder=5)
        #ax.scatter([max_value], [0], color='lightgreen', s=60, zorder=5)

        # Annotate the values directly on the plot
        ax.text(ref_value, 0, f'Ref: {ref_value}', va='center', ha='left', color='black', fontsize=15)
        ax.text(min_value, 0, f'Min: {min_value}', va='center', ha='right', color='skyblue', fontsize=15)
        ax.text(max_value, 0, f'Max: {max_value}', va='center', ha='left', color='lightgreen', fontsize=15)

        # Remove x and y axis labels and ticks
        ax.set_xticks([])  # No x-axis ticks
        ax.set_yticks([])  # No y-axis ticks
        ax.set_xticklabels([])  # No x-axis labels
        ax.set_yticklabels([])  # No y-axis labels

        # Remove frame and grid
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(False)  # No grid lines

        # Set x-axis limits to ensure markers and values fit nicely within the plot
        ax.set_xlim(min(0, min_value - 1), max_value + 1)

        # Return the plot as a Kivy widget (FigureCanvasKivyAgg)
        return FigureCanvasKivyAgg(fig)

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

