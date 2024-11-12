import re

from rapidfuzz import process

from databaseFiles.tables.parameterTable import ParameterTable


class DataExtraction:
    '''Extracts data from an input file'''

    def __init__(self, exam_data):
        self.exam_data = exam_data
        self.parameter_table = ParameterTable()
        self.parameters_names = self.parameter_table.get_parameters_names()
        self.parameters_data = self.parameter_table.get_parameters_data()
        self.formatted_exam_data = self.format_data(exam_data)
        self.filtered_exam_data = self.filter_exam_data(self.formatted_exam_data, self.parameters_names)
        print(self.parameters_names)
        print(self.parameters_data)
        print(self.formatted_exam_data)
        print(self.filtered_exam_data)

    def format_data(self, exam_data):
        '''Formats the given data into proper form'''
        refactored_data = {}
        for key, value in exam_data.items():
            # Find the first numeric value (supports numbers with decimal commas)
            match = re.search(r'\d+,\d+', value)
            if match:
                refactored_data[key] = match.group().replace(',', '.')
        return refactored_data

    def filter_exam_data(self, exam_data, parameters_data, threshold=80):
        '''Filters the exam data and leaves just the information about parameters existing in the database'''
        filtered_data = {}
        for param in parameters_data:
            match = process.extractOne(param, exam_data.keys(), score_cutoff=threshold)
            if match:
                best_match_key, score = match[0], match[1]
                filtered_data[best_match_key] = exam_data[best_match_key]
        return filtered_data


#
# DE = DataExtraction({
#     "Leukocyty (WBC)": "3,24  10^9/  4,0    10,0",
#     "Erytrocyty (RBC)": "4,54  10412儿  4,5    5,5",
#     "Hemoglobina (HGB)": "13,72  gIdl  13,50    18,00",
#     "Hematokryt (HCT)": "41,6  %  40,0"
# })