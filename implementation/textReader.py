import easyocr
import ssl
#import json
from implementation.jsonGenerator import JsonGenerator

# Bypass SSL verification (not recommended for production use)
ssl._create_default_https_context = ssl._create_unverified_context


class TextReader:
    def __init__(self, image_path, languages=['ch_sim', 'en'], quantize=False):
        self.reader = easyocr.Reader(languages, quantize=quantize)
        self.image_path = image_path
        self.results = []

    def read_text(self):
        self.result = self.reader.readtext(self.image_path)
        self._process_text()

    def _process_text(self):
        last_pos = 0
        curr_pos = 0
        string = ""

        for i in range(0, len(self.result) - 1):
            string += str(self.result[i][1]) + "  "
            last_pos = curr_pos
            curr_pos = self.result[i + 1][0][0][1]  # TPikies_magic_numbers
            if curr_pos > last_pos + 10:
                self.results.append(string.strip())
                print(string)
                print()
                string = ""

        # Append the last collected string if any
        if string:
            self.results.append(string.strip())

    def save_to_json(self):
        json_generator = JsonGenerator(self.results)
        return json_generator.save_to_json_text()




