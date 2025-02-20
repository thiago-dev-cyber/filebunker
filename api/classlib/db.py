import os
import sqlite3


class DataBase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)

    def create_tables(self):
        """
        Create a tables of database.
        """
        cursor = self.conn.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS Files (
            id TEXT PRIMARY KEY NOT NULL,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_cksum TEXT NOT NULL,
            file_key TEXT NOT NULL,
            file_iv TEXT NOT NULL
        )
        """
        cursor.execute(sql)
        self.conn.commit()


    def close(self):
        """
        Close connection with database.
        """
        self.conn.close()

    def insert(self, id, file_name, file_path, file_cksum, file_key, file_iv):
        """
        Insert a new metadata file in database.
        """
        cursor = self.conn.cursor()

        try:
            cursor.execute('BEGIN')
            sql = """
	    	INSERT INTO Files (id, file_name, file_path, file_cksum, file_key, file_iv)
	    	VALUES (?, ? , ? , ? ,? ,?)
	    	"""

            cursor.execute(
                sql, (id, file_name, file_path, file_cksum, file_key, file_iv)
            )

            self.conn.commit()

        except sqlite3.Error as err:
            print(f'Fail to insert data {err}')
            self.conn.rollback()


    def remove_by_id(self, file_id):
        cursor = self.conn.connect()
        try:
            sql = """
            DELETE FROM Files WHERE id=?
            """

            cursor.execute(sql, (id,))

            self.conn.commit()

            
        except sqlite3.Error as err:
            print(f"Fail to remove register {err}")


    def fetch_all(self):
        cursor = self.conn.cursor()
        try:
            sql = """
            SELECT * FROM Files ORDER BY file_name
            """

            cursor.execute(sql)

            result = cursor.fetchall()

            return result

        except sqlite3.Error as err:
            print(f"Failt to fetch data {err}")


    def get_file_by_id_or_name(self, id=None, file_name=None):
        cursor = self.conn.cursor()

        try:
            sql = """
            SELECT * FROM Files WHERE file_name=? OR id=?
            """

            cursor.execute(sql, (file_name, id))

            result = cursor.fetchall()

            return result[0]

        except sqlite3.Error as err:
            print(f"Fail to feat data {err}")


