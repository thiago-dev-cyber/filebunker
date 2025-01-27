import os
import secrets
import sys
import threading
from base64 import b64encode


# Ensure parent directory is in sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Import File and FileHelp classes
from api.classlib.db import DataBase
from api.classlib.file import File
from api.classlib.filehelp import FileHelp


ENCRYPT_PATH = os.path.join(os.environ['ROOT'], 'data/encrypt')
CLOUD_PATH = os.path.join(os.environ['ROOT'], 'data/cloud')

if not os.path.exists(ENCRYPT_PATH):
    os.makedirs(ENCRYPT_PATH, exist_ok=True)

if not os.path.exists(CLOUD_PATH):
    os.makedirs(CLOUD_PATH, exist_ok=True)


class Manager:
    """
    Class responsible for managing local files as well as remote files.
    It includes functionalities to manage directories, list files,
    encrypt and upload files,
    download files, and interact with a JSON-based database.
    """

    pool_files = {}
    database = None
    remote_directory = 'pandora'

    @staticmethod
    def _list_files(path: str) -> dict:
        try:
            if not os.path.exists(path):
                raise NotADirectoryError(f'The directory at {path} does not exist.')

            files = {}
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    existing_file = None
                    for path, files in Manager.pool_files.items():
                        for fname, info in files.items():
                            if info['real_path'] == file_path:
                                existing_file = info
                                break
                        if existing_file:
                            break

                    if existing_file:
                        files[file] = existing_file
                    else:
                        files[file] = {
                            'id': FileHelp.gen_file_id(),
                            'cksum': FileHelp.cksum(file_path),
                            'real_path': file_path,
                            'loaded': False,
                        }

            return files

        except NotADirectoryError as err:
            print(f'There was an error trying to list files: {err}')

        except Exception as err:
            print(f'{err}')

        return {}

    @classmethod
    def add_path(cls, path: str):
        """
        Adds a new directory path to the configuration database if it
        exists and is not already added.

        Args:
            path (str): Path that will be added to the configuration file.

        Raises:
            Exception: If the directory does not exist, the database is
            not initialized,
                       or the path is already added.
        """
        try:
            if not os.path.exists(path):
                raise Exception(f'The directory at {path} does not exist.')

            if cls.database is None:
                raise Exception('Database is not initialized.')

            if path not in cls.database.db['paths']:
                cls.database.db['paths'][path] = {}

                files = Manager._list_files(path)

                if files is not None:
                    cls.pool_files[path] = files
                    cls.database.db['paths'][path] = files

                cls.database.save()

            else:
                raise Exception('The directory has already been added.')

        except Exception as err:
            print(f'There was an error trying to add the path: {err}')

    @classmethod
    def init_database(cls, db_path: str, password: str) -> bool:
        """
        Initializes the database by loading it from the specified path
        using a password.

        Args:
            db_path (str): Path to the database file.
            password (str): Password to decrypt and access the database.

        Returns:
            bool: True if the database is successfully loaded, otherwise
            False.

        Raises:
            Exception: If the database file does not exist or there is a
            problem loading it.
        """
        try:
            if not os.path.exists(db_path):
                return False

            cls.database = DataBase.load_db(db_path, password)

            if not cls.database:
                return False

            cls.reload_files_pool()

            return True
        except Exception as err:
            print(f'There was a problem initializing the database: {err}')
            return False

    @classmethod
    def _save(cls):
        """
        Saves the current state of the database to persist changes.
        """
        print(cls.database.db)
        cls.database.save()

    @classmethod
    def upload_files(cls, m_obj: object):
        """
        Encrypts and uploads files to a remote directory using threading
        for parallel processing.

        Args:
            m_obj (object): Remote object manager responsible for handling
            file uploads.

        Raises:
            Exception: If there is an error during the upload process.
        """
        try:

            def process_file(filename, info, data):
                """
                Encrypts and uploads a single file.

                Args:
                    filename (str): Name of the file.
                    info (dict): Metadata of the file.
                    data (str): Directory path containing the file.
                """
                try:
                    f = cls._load_file(info['real_path'])
                    key = b64encode(secrets.token_bytes(32)).decode('utf-8')
                    iv = b64encode(secrets.token_bytes(16)).decode('utf-8')

                    outfile = os.path.join(ENCRYPT_PATH, f.id)

                    cls.pool_files[data][filename]['key'] = key
                    cls.pool_files[data][filename]['iv'] = iv

                    FileHelp.encrypt_file(key, iv, f.path, outfile)
                    m_obj.upload_file(cls.remote_directory, outfile)

                except Exception as err:
                    print(f'Error processing file {filename}: {err}')

            threads = []

            # Create threads for parallel processing
            for data, files in cls.pool_files.items():
                for filename, info in files.items():
                    t = threading.Thread(
                        target=process_file, args=(filename, info, data)
                    )
                    threads.append(t)
                    t.start()

            # Wait for all threads to complete
            for t in threads:
                t.join()

            cls._save()

        except Exception as err:
            print('Unable to upload: ', err)

    # TODO: Finalize the method responsible for downloading
    @classmethod
    def download_files(cls, obj_me: object):
        """
        Downloads files from the remote directory if they are not
        already present locally.

        Args:
            obj_me (object): Remote object manager responsible for
            handling file downloads.
        """
        try:
            local_files = os.listdir(ENCRYPT_PATH)
            print(local_files)
            for data, files in cls.pool_files.items():
                for filename, info in files.items():
                    f = cls._load_file(info['real_path'])
                    if f.id not in local_files:
                        print(f.id)
                        print('File not found')

        except Exception as err:
            print(err)

    @classmethod
    def reload_files(cls):
        """
        Reloads the metadata of all files in the database paths.
        """
        paths = list(cls.database.db['paths'].keys())
        if not paths:
            return False

        for path in paths:
            files = cls._list_files(path)
            cls.database.db['paths'][path] = files

        cls._save()

    @classmethod
    def reload_files_pool(cls):
        """
        Reloads the file pool from the database, updating the
        in-memory structure.

        Raises:
            Exception: If there is an error reloading files
            from the database.
        """
        try:
            cls.pool_files = cls.database.db['paths']

        except Exception as err:
            print(f'Unable to reload files: {err}')

    @classmethod
    def _load_file(cls, real_path: str) -> object:
        """
        Loads file metadata from the pool and returns a
        File object.

        Args:
            real_path (str): Full path of the file.

        Returns:
            File: The corresponding File object.

        Raises:
            Exception: If the file does not exist in the pool.
        """
        try:
            file_name = os.path.basename(real_path)
            file_path = os.path.dirname(real_path)

            if file_name not in cls.pool_files[file_path]:
                raise Exception(f'File not Found {file_name}')

            file_info = cls.pool_files[file_path][file_name]

            file = File(
                id=file_info['id'],
                name=file_name,
                cksum=file_info['cksum'],
                path=real_path,
            )

            return file

        except Exception as err:
            print(f'Unable to load the file: {err}')
