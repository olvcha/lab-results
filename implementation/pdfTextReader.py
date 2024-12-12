from PyPDF2 import PdfReader

from implementation.jsonGenerator import JsonGenerator


class PdfTextReader:
    '''Responsible for reading text from a PDF file.'''
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.extracted_text = self.extract_text_from_pdf()
        self.data = self.parse_lab_results_to_table()

    def extract_text_from_pdf(self):
        '''Extract text from pdf file. Return text.'''
        reader = PdfReader(self.pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        return text

    def parse_lab_results_to_table(self):
        '''Parse the extracted text into a list of strings. Include just non-empty lines.'''
        lines = self.extracted_text.split('\n')

        data = []
        for line in lines:
            line = line.strip()
            if line:  # Only include non-empty lines
                data.append(line)  # Directly append the line as a string

        print(data)  # Debugging: Print the flat list
        return data

    def save_to_json(self):
        '''Save the data to JSON format.'''
        json_generator = JsonGenerator(self.data)

        return json_generator.save_to_json_text()
