import json
import matplotlib.dates as mdates
from datetime import datetime
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivymd.app import MDApp
from matplotlib import pyplot as plt
from databaseFiles.tables.examinationTable import ExaminationTable
from databaseFiles.tables.parameterTable import ParameterTable
from databaseFiles.tables.examinationParameterTable import ExaminationParameterTable
from implementation.globalData import GlobalData


class ParameterChangeGenerator:
    '''Responsible for processing raw data into visualisations in the form of plot.
    Represents the change of the parameters in time'''

    def __init__(self):
        global_data = GlobalData()
        self.user_id = global_data.get_user_id()

        self.examination_table = ExaminationTable()
        self.parameter_table = ParameterTable()
        self.examination_parameter_table = ExaminationParameterTable()

    def plot_parameter_in_time(self, parameter_name, dates, values, min_value, max_value, unit, loinc):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, values, marker='o', linestyle='-', color='b')

        ax.hlines(y=min_value, xmin=dates[0], xmax=dates[-1], colors='red', linestyles='--', label='Min Value')
        ax.hlines(y=max_value, xmin=dates[0], xmax=dates[-1], colors='green', linestyles='--', label='Max Value')

        # Add text annotations for min and max lines
        ax.text(dates[-1], min_value, ' Min', color='red', verticalalignment='center', fontsize=10)
        ax.text(dates[-1], max_value, ' Max', color='green', verticalalignment='center', fontsize=10)

        if len(dates) > 5:
            # Show every second or third date
            step = len(dates) // 3 if len(dates) >= 6 else 2
            selected_dates = dates[::step]
        else:
            selected_dates = dates

        ax.set_xticks(selected_dates)


        ax.set_xlabel('Data')
        ax.set_ylabel(f'Wartość [{unit}]')
        ax.set_title(f'{parameter_name} (LOINC = {loinc})')

        fig.subplots_adjust(bottom=0.15)

        return FigureCanvasKivyAgg(fig)

    def generate_results(self):
        '''Generate a list of results, each containing plot widget with change of parameter values over time.'''
        results = []
        for param_id in self.examination_parameter_table.get_parameter_ids(self.user_id):
            dates = []
            values = []
            parameter_data = self.parameter_table.load_parameter_data(param_id)
            parameter_name = parameter_data[0][1]
            min_value = parameter_data[0][2]
            max_value = parameter_data[0][3]
            unit = parameter_data[0][4]
            loinc_code = parameter_data[0][5]

            for data in self.examination_parameter_table.join_examination_with_examination_parameters(self.user_id,
                                                                                                          param_id):
                parsed_data = datetime.strptime(data[2], "%d-%m-%Y")
                dates.append(parsed_data)
                values.append(float(data[1]))


            if len(values) > 1:
                plot_widget = self.plot_parameter_in_time(parameter_name, dates, values, min_value, max_value,
                                                          unit, loinc_code)
                results.append({
                    "plot_widget": plot_widget
        })

        return results
