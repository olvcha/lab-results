import sqlite3
import os
from kivy.utils import platform


class Database:
    '''This class represents the database for whole app. '''

    def __init__(self):
        self.database_name = 'labResults.db'
        self.create_tables()

    def connection_utility(self):
        '''Connect to the database'''
        connection = sqlite3.connect(self.get_db_path())
        return connection

    def get_db_path(self):
        '''Retrieve the path to the database file.'''
        # Check the platform
        if platform == 'android':
            # from android.storage import app_storage_path
            # storage_dir = app_storage_path()
            # db_path = os.path.join(storage_dir, 'labResults.db')
            pass
        else:
            # Use a relative path
            db_path = os.path.join(os.path.dirname(__file__), 'labResults.db')
        return db_path

    def create_tables(self):
        '''Create the tables in the database if they do not exist.'''
        connection = self.connection_utility()
        cursor = connection.cursor()

        # Enable foreign key constraints in SQLite
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute('''CREATE TABLE IF NOT EXISTS user
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            username TEXT NOT NULL, 
                            password TEXT NOT NULL
                            )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS parameter
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            name TEXT NOT NULL, 
                            min_value INTEGER NOT NULL, 
                            max_value INTEGER NOT NULL,
                            unit TEXT NOT NULL,
                            loinc_code TEXT NOT NULL,
                            priority BOOLEAN NOT NULL
                            )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS examination
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            user_id INTEGER NOT NULL,
                            date DATETIME NOT NULL,
                            data_reference_id TEXT NOT NULL, 
                            data TEXT NOT NULL,
                            FOREIGN KEY(user_id) REFERENCES user(id))''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS examination_parameter 
                            (value TEXT NOT NULL,
                            exam_id INTEGER NOT NULL,
                            parameter_id INTEGER NOT NULL,
                            FOREIGN KEY(exam_id) REFERENCES examination(id),
                            FOREIGN KEY(parameter_id) REFERENCES parameter(id))''')

        connection.commit()
        cursor.close()
        connection.close()

