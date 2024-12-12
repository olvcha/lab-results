import easyocr
import ssl
#import json
from implementation.jsonGenerator import JsonGenerator

# Bypass SSL verification (not recommended for production use)
ssl._create_default_https_context = ssl._create_unverified_context


class TextReader:
    '''Responsible for reading text from an image file.'''
    def __init__(self, image_path, languages=['ch_sim', 'en'], quantize=False):
        self.reader = easyocr.Reader(languages, quantize=quantize)
        self.image_path = image_path
        self.results = []

    def read_text(self):
        '''Read text from image and process it."'''
        self.result = self.reader.readtext(self.image_path)
        self.process_text()

    def process_text(self):
        '''Process data from image using segmentation. Separate all data about parameter from particular line. '''
        last_pos = 0
        curr_pos = 0
        string = ""

        for i in range(0, len(self.result) - 1):
            string += str(self.result[i][1]) + "  "
            last_pos = curr_pos
            curr_pos = self.result[i + 1][0][0][1]
            if curr_pos > last_pos + 10:
                self.results.append(string.strip())
                string = ""

        # Append the last collected string if any
        if string:
            self.results.append(string.strip())

    def save_to_json(self):
        '''Convert data into JSON type variable.'''
        json_generator = JsonGenerator(self.results)
        return json_generator.save_to_json_text()




