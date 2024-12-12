from databaseFiles.tables.userTable import UserTable
from databaseFiles.tables.parameterTable import ParameterTable
from databaseFiles.tables.examinationTable import ExaminationTable
from databaseFiles.database import Database
import json


class DatabaseInitialization:
    '''This class is responsible for data initialization
    Inserts basic data into the tables: user, parameter and examination.
    '''
    def __init__(self):
        self.database = Database()
        #self.userTable = UserTable()
        #self.parameterTable = ParameterTable()
        #self.examinationTable = ExaminationTable()
        self.initialize()

    def initialize(self):
        '''Initialize the data.'''
        #self.initialize_user_table()
        self.initialize_parameter_table()
        #self.initialize_examination_table()
        #self.initialize_examination_parameter_table()

    def initialize_user_table(self):
        '''Initialize the user table data.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        check_query = ("SELECT * FROM user")
        cursor.execute(check_query)
        users = cursor.fetchall()

        if not users:
            add_query_1 = (
                "INSERT INTO user (username, password) VALUES ('Andrzej', 'Andre')")
            add_query_2 = (
                "INSERT INTO user (username, password) VALUES ('Bartosz', 'Barte')")
            cursor.execute(add_query_1)
            cursor.execute(add_query_2)

            connection.commit()
            cursor.close()
            connection.close()

    def initialize_parameter_table(self):
        '''Initialize the parameter table data.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        check_query = ("SELECT * FROM parameter")
        cursor.execute(check_query)
        parameters = cursor.fetchall()

        if not parameters:
            add_query = (    '''INSERT INTO parameter (name, min_value, max_value, unit, loinc_code, priority) 
                                VALUES 
                                ('Erytrocyty (RBC)', 4.2, 5.4, '10^9/l', '789-8', true),
                                ('Leukocyty (WBC)', 4.0, 10.0, '10^12/l','804-5', true),
                                ('Krwinki czerwone (RBC)', 4.2, 5.4, '10^9/l', '789-8', false),
                                ('Krwinki białe (WBC)', 4.0, 10.0, '10^12/l', '804-5', false),
                                ('Hemoglobina (HGB)', 13.0, 18.0, 'g/dl','718-7', true),
                                ('Hematokryt (HCT)', 40.0, 54.0, '%', '20570-8', true),
                                ('MCV', 82.0, 92.0, 'fl', '787-2', true),
                                ('Średnia objętość erytrocyta (MCV)',82.0, 92.0, 'fl', '787-2', false),
                                ('MCH', 27.0, 31.0, 'pg', '785-6', true),
                                ('Średnia masa HGB w erytrocycie (MCH)', 27.0, 31.0, 'pg', '785-6', false),
                                ('MCHC', 32.0, 36.0, 'g/dl','786-4', true),
                                ('Średnie stężenie HGB w erytrocytach (MCHC)', 32.0, 36.0,' g/dl', '786-4', false),
                                ('MPV', 7.5, 10.5, 'fl','32623-1', true),
                                ('Średnia objętość płytki krwi (MPV)', 7.5, 10.5, 'fl', '32623-1', false);
                                ''')

            cursor.execute(add_query)

            connection.commit()
            cursor.close()
            connection.close()

    def initialize_examination_table(self):
        '''Initialize the examination table data.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        check_query = ("SELECT * FROM examination")
        cursor.execute(check_query)
        examinations = cursor.fetchall()

        json_data1 = {
            "Leukocyty (WBC)": "3,24  10^9/  4,0    10,0",
            "Erytrocyty (RBC)": "4,54  10^12/  4,5    5,5",
            "Hemoglobina (HGB)": "13,72  g/dl  13,50    18,00",
            "Hematokryt (HCT)": "41,6  %  40,0"
        }

        json_data2 = {
            "Leukocyty (WBC)": "6,24  10^9/  4,0    10,0",
            "Erytrocyty (RBC)": "6,54  10^12/  4,5    5,5",
            "Hemoglobina (HGB)": "13,72  g/dl  13,50    18,00",
            "Hematokryt (HCT)": "41,6  %  40,0"
        }

        json_data3 = {
            "Leukocyty (WBC)": "5,24  10^9/  4,0    10,0",
            "Erytrocyty (RBC)": "5,54  10^12/  4,5    5,5",
            "Hemoglobina (HGB)": "13,72  g/dl  13,50    18,00",
            "Hematokryt (HCT)": "41,6  %  40,0"
        }

        # Convert the dictionary to a JSON string
        json_string1 = json.dumps(json_data1)
        json_string2 = json.dumps(json_data2)
        json_string3 = json.dumps(json_data3)

        if not examinations:
            add_query_1 = (
                "INSERT INTO examination (user_id, date, data_reference_id, data) VALUES (?, ?, ?, ?)")
            add_query_2 = (
                "INSERT INTO examination (user_id, date, data_reference_id, data) VALUES (?, ?, ?, ?)")
            add_query_3 = (
                "INSERT INTO examination (user_id, date, data_reference_id, data) VALUES (?, ?, ?, ?)")

            cursor.execute(add_query_1, (1, '21-01-2024', '/Users/ola/Documents/Inżynierka/badanie.png', json_string1))
            cursor.execute(add_query_2, (1, '15-06-2024', '/Users/ola/Documents/Inżynierka/badanie.png ', json_string2))
            cursor.execute(add_query_3, (1, '03-11-2024', '/Users/ola', json_string3))

            connection.commit()
            cursor.close()
            connection.close()

    def initialize_examination_parameter_table(self):
        '''Initialize examination parameter data.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        check_query = ("SELECT * FROM examination_parameter")
        cursor.execute(check_query)
        parameters = cursor.fetchall()

        if not parameters:
            add_query_1 = (
                "INSERT INTO examination_parameter (value, exam_id, parameter_id) VALUES ('3.24', 1, 2)")
            add_query_2 = (
                "INSERT INTO examination_parameter (value, exam_id, parameter_id) VALUES ('4.54', 1, 1)")
            add_query_3 = (
                "INSERT INTO examination_parameter (value, exam_id, parameter_id) VALUES ('6.24', 2, 2)")
            add_query_4 = (
                "INSERT INTO examination_parameter (value, exam_id, parameter_id) VALUES ('6.54', 2, 1)")
            add_query_5 = (
                "INSERT INTO examination_parameter (value, exam_id, parameter_id) VALUES ('5.24', 3, 2)")
            add_query_6 = (
                "INSERT INTO examination_parameter (value, exam_id, parameter_id) VALUES ('5.54', 3, 1)")

            cursor.execute(add_query_1)
            cursor.execute(add_query_2)
            cursor.execute(add_query_3)
            cursor.execute(add_query_4)
            cursor.execute(add_query_5)
            cursor.execute(add_query_6)

            connection.commit()
            cursor.close()
            connection.close()
