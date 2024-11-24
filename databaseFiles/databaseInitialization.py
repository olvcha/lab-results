from databaseFiles.tables.userTable import UserTable
from databaseFiles.tables.parameterTable import ParameterTable
from databaseFiles.tables.examinationTable import ExaminationTable
from database import Database
from datetime import datetime
import json


class DatabaseInitialization:
    '''This class is responsible for data initialization
    Inserts basic data into the tables: user, parameter and examination.
    '''
    def __init__(self):
        self.userTable = UserTable()
        self.parameterTable = ParameterTable()
        self.examinationTable = ExaminationTable()
        self.database = Database()

        self.initialize()

    def initialize(self):
        '''This method initializes the data'''
        self.initialize_user_table()
        self.initialize_parameter_table()
        self.initialize_examination_table()

    def initialize_user_table(self):
        '''This method is responsible for initializing the user table data'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        check_query = ("SELECT * FROM user")
        cursor.execute(check_query)
        users = cursor.fetchall()

        if not users:
            add_query_1 = (
                "INSERT INTO user (username, password) VALUES ('andrzej', 'kabanos')")
            add_query_2 = (
                "INSERT INTO user (username, password) VALUES ('anna', 'maria')")
            cursor.execute(add_query_1)
            cursor.execute(add_query_2)

            connection.commit()
            cursor.close()
            connection.close()

    def initialize_parameter_table(self):
        '''This method is responsible for initializing the parameter table data'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        check_query = ("SELECT * FROM parameter")
        cursor.execute(check_query)
        parameters = cursor.fetchall()

        if not parameters:
            add_query_1 = (
                "INSERT INTO parameter (id, name, min_value, max_value, loinc_code) VALUES (1, 'Erytrocyty', 4.7, 6.1, '789-8')")
            add_query_2 = (
                "INSERT INTO parameter (id, name, min_value, max_value, loinc_code) VALUES (2, 'Leukocyty', 4.0, 10.0, '34445-7')")

            cursor.execute(add_query_1)
            cursor.execute(add_query_2)

            connection.commit()
            cursor.close()
            connection.close()

    def initialize_examination_table(self):
        '''This method is responsible for initializing the examination table data'''
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
                "INSERT INTO examination (user_id, date, data_reference, data) VALUES (?, ?, ?, ?)")
            add_query_2 = (
                "INSERT INTO examination (user_id, date, data_reference, data) VALUES (?, ?, ?, ?)")
            add_query_3 = (
                "INSERT INTO examination (user_id, date, data_reference, data) VALUES (?, ?, ?, ?)")

            # Execute the insert queries with appropriate parameters
            cursor.execute(add_query_1, (1, '2024-01-21 12:06', '/Users/ola/Documents/Inżynierka/badanie.png', json_string1))
            cursor.execute(add_query_2, (1, '2024-06-21 18:06', '/Users/ola/Documents/Inżynierka/badanie.png ', json_string2))
            cursor.execute(add_query_3, (1, '2024-11-21 22:06', '/Users/ola', json_string3))

            connection.commit()
            cursor.close()
            connection.close()


init = DatabaseInitialization()
