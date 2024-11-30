import json
import matplotlib.dates as mdates
from datetime import datetime
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivymd.app import MDApp
from matplotlib import pyplot as plt
from databaseFiles.tables.examinationTable import ExaminationTable
from databaseFiles.tables.parameterTable import ParameterTable
from databaseFiles.tables.examinationParameterTable import ExaminationParameterTable
from implementation.dataExtraction import DataExtraction
from implementation.globalData import GlobalData


class ParameterChangeGenerator:
    '''Responsible for processing raw data into visualisations in the form of plot.
    Represents the change of the parameters in time'''

    def __init__(self):
        # app = MDApp.get_running_app()
        # self.user_id = app.get_user_id()
        global_data = GlobalData()
        self.user_id = global_data.get_user_id()

        self.examination_table = ExaminationTable()
        self.parameter_table = ParameterTable()
        self.examination_parameter_table = ExaminationParameterTable()

        #self.exam_data = self.examination_parameter_table.get_examination_parameters_by_exam_id()
        #print(self.exam_data)
        #self.parameter_change_data = self.initialize_parameter_change_data()
        self.generate_results()


    # def initialize_parameter_change_data(self):
    #     refactored_data = {}
    #     for parameter in self.parameter_table.get_parameters_names():
    #         parameter_values_data = {}
    #         for record in self.exam_data:
    #             try:
    #                 json_str = record[4]
    #                 exam_data = json.loads(json_str)
    #                 data_extraction = DataExtraction(exam_data)
    #
    #                 # Try to access the parameter in the filtered exam data
    #                 parameter_value = data_extraction.get_filtered_exam_data()[parameter]
    #
    #                 # If no exception, store the result
    #                 parameter_values_data[record[0]] = (record[2], parameter_value)
    #
    #             except KeyError:
    #                 # If the parameter doesn't exist, skip this record and continue with the next one
    #                 print(f"KeyError: Parameter '{parameter}' not found in record {record[0]}. Skipping.")
    #                 continue
    #             except Exception as e:
    #                 # Catch any other exception, log it, and continue
    #                 print(f"Error processing record {record[0]}: {e}. Skipping.")
    #                 continue
    #
    #         refactored_data[parameter] = parameter_values_data
    #
    #     print("git czy nei git????", refactored_data)
    #     return refactored_data

    #TO_DO: markery dla wartosci min i max, wyroznienie aktualnego wyniku, wartosci miesiecy na osi x
    def plot_parameter_in_time(self, parameter_name, dates, values, min_value, max_value, loinc):
        # Create the matplotlib plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, values, marker='o', linestyle='-', color='b')  # Blue line with circle markers

        ax.hlines(y=min_value, xmin=dates[0], xmax=dates[-1], colors='red', linestyles='--', label='Min Value')
        ax.hlines(y=max_value, xmin=dates[0], xmax=dates[-1], colors='green', linestyles='--', label='Max Value')

        # Add text annotations for min and max lines
        ax.text(dates[-1], min_value, ' Min', color='red', verticalalignment='center', fontsize=10)
        ax.text(dates[-1], max_value, ' Max', color='green', verticalalignment='center', fontsize=10)

        ax.set_xlabel('Data')
        ax.set_ylabel('Wartość')
        ax.set_title(f'{parameter_name} (LOINC = {loinc})')

        fig.subplots_adjust(bottom=0.15)

        return FigureCanvasKivyAgg(fig)

    def generate_results(self):
        results = []
        for param_id in self.examination_parameter_table.get_parameter_ids(self.user_id):
            dates = []
            values = []
            parameter_data = self.parameter_table.load_parameter_data(param_id)
            parameter_name = parameter_data[0][1]
            min_value = parameter_data[0][2]
            max_value = parameter_data[0][3]
            loinc = parameter_data[0][4]

            for data in self.examination_parameter_table.join_examination_with_examination_parameters(self.user_id, param_id):
                dates.append(data[2])
                values.append(float(data[1]))

            plot_widget = self.plot_parameter_in_time(parameter_name, dates, values, min_value, max_value, loinc)
            results.append({
                "plot_widget": plot_widget
            })


        return results




