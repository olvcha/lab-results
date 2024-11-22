import json

from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivymd.app import MDApp
from matplotlib import pyplot as plt
from databaseFiles.tables.examinationTable import ExaminationTable
from databaseFiles.tables.parameterTable import ParameterTable
from implementation.dataExtraction import DataExtraction


class ParameterChangeGenerator:
    '''Responsible for processing raw data into visualisations in the form of plot.
    Represents the change of the parameters in time'''

    def __init__(self):
        app = MDApp.get_running_app()
        self.user_id = app.get_user_id()
        self.examination_table = ExaminationTable()
        self.parameter_table = ParameterTable()

        self.exam_data = self.examination_table.fetch_examination_data(self.user_id)
        print(self.exam_data)
        self.parameter_change_data = self.initialize_parameter_change_data()
        self.generate_results()


    def initialize_parameter_change_data(self):
        refactored_data = {}
        for parameter in self.parameter_table.get_parameters_names():
            parameter_values_data={}
            for record in self.exam_data:
                json_str = record[4]
                exam_data = json.loads(json_str)
                data_extraction = DataExtraction(exam_data)
                parameter_values_data[record[0]] = (record[2], data_extraction.get_filtered_exam_data()[parameter])
            refactored_data[parameter] = parameter_values_data

        print("git czy nei git????", refactored_data)
        return refactored_data

    #TO_DO: markery dla wartosci min i max, wyroznienie aktualnego wyniku, wartosci miesiecy na osi x
    def plot_parameter_in_time(self, dates, values):
        # Create the matplotlib plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(dates, values, marker='o', linestyle='-', color='b')  # Blue line with circle markers
        ax.set_xlabel('Date')
        ax.set_ylabel('Value')
        ax.set_title('Parameter Values Over Time')

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45)

        return FigureCanvasKivyAgg(fig)

    def generate_results(self):
        results = []
        for parameter, data in self.parameter_change_data.items():
            dates = []
            values = []

            for record in data.values():
                date, value = record
                dates.append(date)
                values.append(float(value))

            plot_widget = self.plot_parameter_in_time(dates, values)

            results.append({
                "param_name": parameter,
                "plot_widget": plot_widget
            })

        return results




