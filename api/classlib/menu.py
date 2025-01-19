import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from uuid import uuid4

from api.classlib.filehelp import FileHelp


class Manager:
    """
    Class responsible for managing local files as well as remote files.
    """

    @staticmethod
    def add_path(path: str, database: object):
        """
        Method responsible for adding a new directory path to a JSON config file.


        Args:
            path (str): Path that will be added to the configuration file.
            database (object): Configuration file instance.


        """
        try:
            if not os.path.exists(path):
                raise Exception(f'The directory at {path} does not existis.')

            if path not in database.db['paths']:
                database.db['paths'][path] = {}

                files = Manager._list_files(path)

                if files is not None:
                    for file in files:
                        real_path = os.path.join(path, file)
                        cksum = FileHelp.cksum(real_path)
                        id = str(uuid4())

                        database.db['paths'][path][file] = {
                            'id': id,
                            'cksum': cksum,
                            'path': real_path,
                        }

                database.save()

            else:
                raise Exception('The directory has already been added')

        except Exception as err:
            print(f'There was an error trying to adding path: {err}')

    @staticmethod
    def upload_files():
        pass

    @staticmethod
    def download_files():
        pass

    @staticmethod
    def _list_files(path: str):
        try:
            if not os.path.exists(path):
                raise NotADirectoryError(f'The directory at {path} does not exists.')

            files = []
            for file in os.listdir(path):
                if os.path.isfile(os.path.join(path, file)):
                    files.append(file)

            return files

        except NotADirectoryError as err:
            print(f'There was an error trying to list files: {err}')

        except Exception as err:
            print(f'{err}')

        else:
            return []
