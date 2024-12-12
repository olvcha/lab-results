import json
import re

from rapidfuzz import process

from databaseFiles.tables.parameterTable import ParameterTable


class DataExtraction:
    '''Responsible for extracting data.'''
    def __init__(self, exam_data):
        self.exam_data = json.loads(exam_data)
        self.formatted_data = self.format_data()
        self.parameter_table = ParameterTable()
        self.parameters_data = self.parameter_table.get_parameters_names_and_ids()

    def format_data(self):
        '''Format the given data into the form parameter name : value.'''
        refactored_data = {}
        for key, value in self.exam_data.items():
            # Find the first numeric value (supports numbers with decimal commas)
            match = re.search(r'\d+,\d+', value)
            if match:
                refactored_data[key] = match.group().replace(',', '.')
        return refactored_data

    def filter_exam_data(self, threshold=80):
        '''Filter the exam data and leave just the information about parameters existing in the database.
        Return tuple of exam data in format value : parameter_id.'''
        filtered_data = {}
        for id, name in self.parameters_data:
            match = process.extractOne(name, self.formatted_data.keys(), score_cutoff=threshold)
            if match:
                best_match_key, score = name, id
                filtered_data[score] = self.formatted_data[match[0]]
        return filtered_data

