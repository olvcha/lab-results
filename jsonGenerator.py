import re
import json


class JsonGenerator:
    def __init__(self, data, file_name):
        self.data = data
        self.file_name = file_name
        self.parse_data()
        self.save_to_json()

    def parse_data(self):
        parsed_data = {}
        for entry in self.data:
            # Match the initial text (key) and the rest of the entry (value)
            match = re.match(r"([^\d]+)\s+([\d,]+.*)", entry)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                parsed_data[key] = value

        return parsed_data

    def save_to_json(self):
        parsed_data = self.parse_data()
        with open(self.file_name, 'w', encoding='utf-8') as json_file:
            json.dump(parsed_data, json_file, ensure_ascii=False, indent=4)

    def save_to_json_text(self):
        parsed_data = self.parse_data()

        return json.dumps(parsed_data, ensure_ascii=False)





