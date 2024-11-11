import sqlite3
import os
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore


class Database:
    '''This class represents the database for whole app. '''

    def __init__(self):
        self.database_name = 'labResults.db'
        self.create_tables()

    def connection_utility(self):
        '''This method is used to connect to the database'''
        connection = sqlite3.connect(self.get_db_path())
        return connection

    def get_db_path(self):
        # Check the platform
        if platform == 'android':
            # Get the Android app's internal storage path
            #from android.storage import app_storage_path
            #storage_dir = app_storage_path()
            #db_path = os.path.join(storage_dir, 'labResults.db')
            pass
        else:
            # For desktop or other platforms, use a relative path
            db_path = os.path.join(os.path.dirname(__file__), 'labResults.db')
            print(db_path)
        return db_path

    def create_tables(self):
        '''This method creates the tables in the database if they do not exist'''
        connection = self.connection_utility()
        cursor = connection.cursor()

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
                            loinc_code TEXT NOT NULL
                            )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS examination
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            user_id INTEGER NOT NULL,
                            data_reference TEXT NOT NULL, 
                            data TEXT NOT NULL)''')

        connection.commit()
        cursor.close()
        connection.close()

database = Database()