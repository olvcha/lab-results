import _sqlite3
from databaseFiles.database import Database


class ParameterTable:
    '''This class represent a parameter table in the database.
    Enables information retrieval and insertion into the parameter table.'''

    def __init__(self):
        self.database = Database()

    def add_parameter(self, parameter_id, name, min_value, max_value, unit, loinc_code, priority):
        '''Insert a new parameter into the database.'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("INSERT INTO parameter (id, name, min_value, max_value, unit, loinc_code, priority) VALUES (?, ?, ?, ?, ?, ?, ?)")
        cursor.execute(query, (parameter_id, name, min_value, max_value, unit, loinc_code, priority))

        connection.commit()
        cursor.close()
        connection.close()

    def load_parameter_data(self, parameter_id):
        '''Load the data of selected parameter from the database.
        Data is returned as a tuple in order: name, min_value, max_value, loinc_code, priority.'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT * FROM parameter WHERE id = ?")
        cursor.execute(query, (parameter_id,))
        parameter_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return parameter_data

    def get_parameters_names(self):
        '''Fetch all parameters' names from the database.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT name FROM parameter")
        cursor.execute(query)

        names = tuple(name[0] for name in cursor.fetchall())

        cursor.close()
        connection.close()

        return names

    def get_parameters_names_and_ids(self):
        '''Fetch all parameters' names and ids.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT id, name FROM parameter")
        cursor.execute(query)
        parameters_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return parameters_data

    def get_parameters_data(self):
        '''Fetch all data about parameters.'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT * FROM parameter")
        cursor.execute(query)
        parameters_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return parameters_data

    def get_priority_parameter(self, parameter_id):
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT loinc_code FROM parameter WHERE id = ?")
        cursor.execute(query, (parameter_id,))
        loinc = cursor.fetchall()[0][0]

        query = ("SELECT id FROM parameter WHERE priority = 1 AND loinc_code = ?")
        cursor.execute(query, (loinc,))
        priority_id = cursor.fetchall()[0]

        cursor.close()
        connection.close()

        return priority_id

