import sqlite3
from databaseFiles.database import Database


class UserTable:
    '''This class represents a user table in the database.
    Enables information retrieval and insertion into the user table.'''

    def __init__(self):
        self.database = Database()

    def add_user(self, username, password):
        '''This method inserts a new user into the database'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("INSERT INTO user (username, password) VALUES (?, ?)")
        cursor.execute(query, (username, password))

        connection.commit()
        cursor.close()
        connection.close()

    def fetch_users(self):
        '''This method fetches all users from the database'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT * FROM user")
        cursor.execute(query)
        users = cursor.fetchall()

        cursor.close()
        connection.close()

        return users

    def auth_user(self, username, password):
        '''This method authenticates the user.
        Returns true if given username and password are correct and false if username and password are incorrect'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT password FROM user WHERE username = ?")
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()

        cursor.close()
        connection.close()

        if user_data:
            if user_data[0] == password:
                return self.get_user(username)
            else:
                return False

    def get_user(self, username):
        '''Gets the user identified by username and password'''

        connection = self.database.connection_utility()
        cursor = connection.cursor()

        query = ("SELECT id FROM user WHERE username = (?)")
        cursor.execute(query, (username,))
        user_id = cursor.fetchone()
        id = user_id[0]

        cursor.close()
        connection.close()

        return id
