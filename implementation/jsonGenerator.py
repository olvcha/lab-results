import re
import json


class JsonGenerator:
    '''Responsible for generating JSON from text.'''
    def __init__(self, data):
        self.data = data
        self.parse_data()

    def parse_data(self):
        '''
        Parse given data into JSON format:
        key - parameter name
        value - parameter data
        '''

        parsed_data = {}
        for entry in self.data:
            # Match the initial text (key) and the rest of the entry (value)
            match = re.match(r"([^\d]+)\s+([\d,]+.*)", entry)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                parsed_data[key] = value

        return parsed_data

    def save_to_json_text(self):
        '''Save to JSON.'''
        parsed_data = self.parse_data()

        return json.dumps(parsed_data, ensure_ascii=False)





