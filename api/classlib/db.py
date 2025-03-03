import mysql.connector
from mysql.connector import errorcode
from mysql.connector import pooling


class DataBase:
    def __init__(self, host, user, port, password, database):
        self.dbconfig = {
            "host": host,
            "user": user,
            "port": port,
            "password": password,
            "database": database
        }

        self.cnxpool = pooling.MySQLConnectionPool(
            pool_name="connections",
            pool_size=10,
            **self.dbconfig
        )

        self.create_tables()

    def get_connection(self):
        return self.cnxpool.get_connection()
        
    def create_tables(self):
        """
        Create tables in the database.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            sql = """
            CREATE TABLE IF NOT EXISTS Files (
                id VARCHAR(255) PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                file_path VARCHAR(255) NOT NULL,
                file_cksum VARCHAR(255) NOT NULL,
                file_key VARCHAR(255) NOT NULL,
                file_iv VARCHAR(255) NOT NULL,
                file_size VARCHAR(255) NOT NULL
            )
            """
            cursor.execute(sql)
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Error creating tables: {err}")

        finally:
            conn.close()

    def fetch(self, id=None, file_cksum=None, file_name=None):
        """
        Fetch metadata from the database.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            params = []
            conditions = []

            if id is not None:
                params.append(id)
                conditions.append('id = %s')

            if file_name is not None:
                params.append(file_name)
                conditions.append('file_name = %s')

            if file_cksum is not None:
                params.append(file_cksum)
                conditions.append('file_cksum = %s')

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

        except mysql.connector.Error as err:
            print(f'Fail: {err}')
        finally:
            conn.close()

    def insert(self, id, file_name, file_path, file_cksum, file_key, file_iv, file_size):
        """
        Insert a new metadata file into the database.
        """
        conn = self.get_connection()  # Use self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('BEGIN')
            sql = """
            INSERT INTO Files (id, file_name, file_path, file_cksum, file_key, file_iv, file_size)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (id, file_name, file_path, file_cksum, file_key, file_iv, file_size))
            conn.commit()

        except mysql.connector.Error as err:
            print(f'Fail to insert data: {err}')
            conn.rollback()

        finally:
            conn.close()

    def remove_by_id_or_name(self, file_id):
        """
        Delete a file.
        """
        conn = self.get_connection()  # Use self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('BEGIN')
            sql = "DELETE FROM Files WHERE id=%s"
            cursor.execute(sql, (file_id,))
            conn.commit()
            return True

        except mysql.connector.Error as err:
            conn.rollback()
            print(f'Fail to remove record: {err}')
            return False

        finally:
            conn.close()

    def fetch_all(self, page=1, limit=10):
        """
        Fetch all file metadata from the database.
        """
        conn = self.get_connection()  # Use self.get_connection()
        cursor = conn.cursor()
        try:
            offset = (page - 1) * limit

            sql = """SELECT * 
            FROM Files ORDER BY file_name
            LIMIT %s OFFSET %s
            """
            cursor.execute(sql, (limit, offset))
            
            result = cursor.fetchall()
            return result

        except mysql.connector.Error as err:
            print(f'Fail to fetch data: {err}')
        finally:
            conn.close()

    def get_file_by_id_or_name(self, id=None, file_name=None):
        """
        Fetch file metadata by id or file_name.
        """
        conn = self.get_connection()  # Use self.get_connection()
        cursor = conn.cursor()

        try:
            sql = "SELECT * FROM Files WHERE file_name=%s OR id=%s"
            cursor.execute(sql, (file_name, id))
            result = cursor.fetchall()
            return result[0] if result else None

        except mysql.connector.Error as err:
            print(f'Fail to fetch data: {err}')
        finally:
            conn.close()
