from PyPDF2 import PdfReader

from implementation.jsonGenerator import JsonGenerator


class PdfTextReader:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.extracted_text = self.extract_text_from_pdf()
        self.data = self.parse_lab_results_to_table()

    def extract_text_from_pdf(self):
        '''Extract text from pdf file. Return that text.'''
        reader = PdfReader(self.pdf_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

        return text

    def parse_lab_results_to_table(self):
        '''Parse the extracted text into a flat list of strings.'''
        lines = self.extracted_text.split('\n')

        # Create a flat list instead of a list of lists
        data = []
        for line in lines:
            line = line.strip()
            if line:  # Only include non-empty lines
                data.append(line)  # Directly append the line as a string

        print(data)  # Debugging: Print the flat list
        return data

    def save_to_json(self):
        json_generator = JsonGenerator(self.data)

        return json_generator.save_to_json_text()
#
# dd = PdfTextReader('/Users/ola/Repos/lab-results/krew.pdf')
# print(dd.save_to_json())