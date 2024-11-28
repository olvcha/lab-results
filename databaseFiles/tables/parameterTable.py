import _sqlite3
from databaseFiles.database import Database


class ParameterTable:
    '''This class represent a parameter table in the database.
    Enables information retrieval and insertion into the parameter table.'''

    def __init__(self):
        self.database = Database()

    def add_parameter(self, parameter_id, name, min_value, max_value, loinc_code):
        '''This method inserts a new parameter into the database'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("INSERT INTO parameter (id, name, min_value, max_value, loinc_code) VALUES (?, ?, ?, ?, ?)")
        cursor.execute(query, (parameter_id, name, min_value, max_value, loinc_code))

        connection.commit()
        cursor.close()
        connection.close()

    def load_parameter_data(self, parameter_id):
        '''This method loads the data of selected parameter from the database.
        Data is returned as a tuple in order: name, min_value, max_value, loinc_code, gender.'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT * FROM parameter WHERE parameter_id = ?")
        cursor.execute(query, (parameter_id))
        parameter_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return parameter_data

    def get_parameters_names(self):
        '''Fetches all parameters' names from the database'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT name FROM parameter")
        cursor.execute(query)

        names = tuple(name[0] for name in cursor.fetchall())

        cursor.close()
        connection.close()

        return names

    def get_parameters_data(self):
        '''Fetches all parameters'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT * FROM parameter")
        cursor.execute(query)
        parameters_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return parameters_data


