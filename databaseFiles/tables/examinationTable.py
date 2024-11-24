import sqlite3
from databaseFiles.database import Database


class ExaminationTable:
    '''Representation of an examination table in the database.
    Enables information retrieval and insertion into the examination table.'''

    def __init__(self):
        self.database = Database()

    def add_examination(self, user_id, date, data_reference, data):
        '''Insert a new examination into the database'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("INSERT INTO examination (user_id, date, data_reference, data) VALUES (?, ?, ?, ?)")
        cursor.execute(query, (user_id, date, data_reference, data))

        last_inserted_id = cursor.lastrowid

        connection.commit()
        cursor.close()
        connection.close()

        return last_inserted_id

    # def load_examination_data(self, examination_id):
    #     '''Load the data of selected examination from the database.
    #     Data is returned in order: parameter_name, reference_value, min_value, max_value'''
    #
    #     connection = self.database.connection_utility()
    #     cursor = connection.cursor()
    #
    #     query = ("SELECT data FROM examination WHERE id = ?")
    #     cursor.execute(query, (examination_id,))
    #     examination_data = cursor.fetchall()
    #
    #     cursor.close()
    #     connection.close()
    #
    #     return examination_data

    def load_examination_data(self, examination_id):
        '''Load the data of selected examination from the database.
        Data is returned in order: parameter_name, reference_value, min_value, max_value'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT * FROM examination WHERE id = ?")
        cursor.execute(query, (examination_id,))
        examination_data = cursor.fetchall()

        user_id = examination_data[0][1]
        date = examination_data[0][2]
        data_reference = examination_data[0][3]
        data = examination_data[0][4]

        cursor.close()
        connection.close()

        examination_tuple = (user_id, date, data_reference, data)

        return examination_tuple

    def fetch_examination_data(self, user_id):
        '''Fetch all examination data for certain user'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT * FROM examination WHERE user_id = ?")
        cursor.execute(query, (user_id,))
        examination_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return examination_data


db = ExaminationTable()
print(db.load_examination_data("1"))
print(db.fetch_examination_data("1"))

