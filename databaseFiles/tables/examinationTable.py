import sqlite3
from databaseFiles.database import Database


class ExaminationTable:
    '''This class represent a examination table in the database.
    Enables information retrieval and insertion into the examination table.'''

    def __init__(self):
        self.database = Database()

    def add_examination(self, user_id, date, data_reference, data):
        '''This method inserts a new examination into the database'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("INSERT INTO examination (user_id, date, data_reference, data) VALUES (?, ?, ?, ?)")
        cursor.execute(query, (user_id, date, data_reference, data))

        last_inserted_id = cursor.lastrowid

        connection.commit()
        cursor.close()
        connection.close()

        return last_inserted_id

    def load_examination_data(self, examination_id):
        '''This method loads the data of selected examination from the database.
        Data is returned as a tuple in order: user_id, data_reference, data.'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT data FROM examination WHERE id = ?")
        cursor.execute(query, (examination_id,))
        examination_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return examination_data

    def fetch_examination_data(self, user_id):
        '''Fetches all examination data for certain user'''
        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT id, date FROM examination WHERE user_id = ?")
        cursor.execute(query, (user_id,))
        examination_data = cursor.fetchall()

        cursor.close()
        connection.close()

        return examination_data


