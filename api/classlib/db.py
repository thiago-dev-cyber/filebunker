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

    def fetch(self, id=None, file_cksum=None, file_name=None):
        """
        Featch metadata in database
        """

        cursor = self.conn.cursor()

        try:
            params = []
            conditions = []

            if id is not None:
                params.append(id)
                conditions.append('id = ?')

            if file_name is not None:
                params.append(file_name)
                conditions.append('file_name = ?')

            if file_cksum is not None:
                params.append(file_cksum)
                conditions.append('file_cksum = ?')

            if not params or not conditions:
                raise ValueError(
                    'At least one parameter (id, file_cksum, file_name) must be provided.'
                )

            sql = f"""
            SELECT id, file_name, file_cksum
            FROM Files
            WHERE {' AND '.join(conditions)}
            """

            cursor.execute(sql, tuple(params))

            return cursor.fetchone()

        except sqlite3.Error as err:
            print(f'Fail: {err}')

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


    def remove_by_id_or_name(self, file_id):
        """
        Delete file.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute('BEGIN')
            sql = """
            DELETE FROM Files WHERE id=?
            """

            cursor.execute(sql, (file_id,))

            self.conn.commit()

            return True

        except sqlite3.Error as err:
            self.conn.rollback()
            print(f'Fail to remove register {err}')
            return False

    def fetch_all(self):
        # TODO: adding pagination.
        """
        fetch all file metadata in databese.
        """
        cursor = self.conn.cursor()
        try:
            sql = """
            SELECT * FROM Files ORDER BY file_name
            """

            cursor.execute(sql)

            result = cursor.fetchall()

            return result

        except sqlite3.Error as err:
            print(f'Failt to fetch data {err}')


    def get_file_by_id_or_name(self, id=None, file_name=None):
        """
        fetch file metadata in database.
        """
        cursor = self.conn.cursor()

        try:
            sql = """
            SELECT * FROM Files WHERE file_name=? OR id=?
            """

            cursor.execute(sql, (file_name, id))

            result = cursor.fetchall()

            return result[0]

        except sqlite3.Error as err:
            print(f'Fail to feat data {err}')
