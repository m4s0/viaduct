from os import getenv

from mysql import connector
from mysql.connector import errorcode, Error


class Database:
    def __init__(self):
        try:
            cnx_config = {
                'username': getenv('DATABASE_USER'),
                'password': getenv('DATABASE_PASSWORD'),
                'host': getenv('DATABASE_HOST'),
                'database': getenv('DATABASE_NAME')
            }

            cnx = connector.connect(**cnx_config)
            print('Connected to MySQL')

        except connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err.msg)
            raise err

        self.connection = cnx
        self.cursor = None

    def execute_query(self, query, values=None, multi=False):
        cursor = self.connection.cursor(dictionary=True)

        try:
            cursor.execute(query, values, multi=multi)
            result = cursor.fetchone()
            cursor.close()
            self.connection.commit()

            return result
        except Error as e:
            print(f"Failed to execute query: {query} with values: {values}")

            if cursor is not None:
                cursor.close()

            self.connection.rollback()
            raise DatabaseException(e.msg)

    def execute_select_for_update(self, query, values):
        self.cursor = self.connection.cursor(dictionary=True)

        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()

            return result
        except Error as e:
            print(f"Failed to execute query: {query} with values: {values}")

            if self.cursor is not None:
                self.cursor.close()

            self.connection.rollback()
            raise DatabaseException(e.msg)


class DatabaseException(Exception):
    pass
