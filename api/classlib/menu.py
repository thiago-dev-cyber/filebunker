import os
import sys


# Ensure parent directory is in sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Import File and FileHelp classes
from api.classlib.file import File
from api.classlib.filehelp import FileHelp


class Manager:
    """
    Class responsible for managing local files as well as remote files.
    """

    pool_files = {}

    @classmethod
    def add_path(cls, path: str, database: object):
        """
        Method responsible for adding a new directory path to a JSON config file.

        Args:
            path (str): Path that will be added to the configuration file.
            database (object): Configuration file instance.
        """
        try:
            if not os.path.exists(path):
                raise Exception(f'The directory at {path} does not exist.')

            if path not in database.db['paths']:
                database.db['paths'][path] = {}

                files = Manager._list_files(path)

                if files is not None:
                    cls.pool_files[path] = files
                    database.db['paths'][path] = files
                    # print(cls.pool_files)

                database.save()

            else:
                raise Exception('The directory has already been added.')

        except Exception as err:
            print(f'There was an error trying to add the path: {err}')

    @staticmethod
    def upload_files():
        pass

    @staticmethod
    def download_files():
        pass

    @staticmethod
    def _list_files(path: str) -> dict:
        try:
            if not os.path.exists(path):
                raise NotADirectoryError(f'The directory at {path} does not exist.')

            files = {}
            # {database.txt: {id:1, cksum: afaf1f3f1, loaded:false}}
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                if os.path.isfile(file_path):
                    if file not in Manager.pool_files:
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

        return files

    @classmethod
    def reload_files(cls, db: object):
        """
        Reloads files into memory from JSON.

        Args:
            db (object): Database Instance.

        Returns:
            None
        """
        try:
            cls.pool_files = db.db['paths']

        except Exception as err:
            print(f'Unable to reload files: {err}')

    @classmethod
    def _load_file(cls, file_path: str) -> object:
        """
        Method responsible for uploading a file when it is requested.

        Args:
            file_path (str): Full path of the file that will be uploaded.
        """
        try:
            file_name = os.path.basename(file_path)
            file_path = os.path.dirname(file_path)

            if file_name not in cls.pool_files[file_path]:
                raise Exception(f'File not Found {file_name}')

            file_info = cls.pool_files[file_path][file_name]

            file = File(
                id=file_info['id'],
                name=file_name,
                cksum=file_info['cksum'],
                path=file_info['real_path'],
            )

            return file

        except Exception as err:
            print(f'Unable to upload the file: {err}')
