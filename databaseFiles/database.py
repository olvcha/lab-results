import sqlite3


class Database:
    '''This class represents the database for whole app. '''

    def __init__(self):
        self.database_name = 'labResults.db'
        self.create_tables()

    def connection_utility(self):
        '''This method is used to connect to the database'''
        connection = sqlite3.connect(self.database_name)
        return connection

    def create_tables(self):
        '''This method creates the tables in the database if they do not exist'''
        connection = self.connection_utility()
        cursor = connection.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS user
                            (id INTEGER PRIMARY KEY NOT NULL, 
                            username TEXT NOT NULL, 
                            password TEXT NOT NULL,
                            gender TEXT NOT NULL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS parameter
                            (id INTEGER PRIMARY KEY NOT NULL, 
                            name TEXT NOT NULL, 
                            min_value INTEGER NOT NULL, 
                            max_value INTEGER NOT NULL,
                            loinc_code TEXT NOT NULL,
                            gender TEXT NOT NULL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS examination
                            (id INTEGER PRIMARY KEY d, 
                            user_id INTEGER NOT NULL,
                            data_reference TEXT NOT NULL, 
                            data TEXT NOT NULL)''')

        connection.commit()
        cursor.close()
        connection.close()

database = Database()