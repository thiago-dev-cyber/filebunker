import os
from time import sleep

from mega import Mega


class ConnectMega:
    """
    A class responsible for managing the connection, sending and downloads
    of mega files.
    """

    def __init__(self, email: str, password: str):
        """
        Initialization object.

        Args:
                email (str): User authentication email.
                password (str): User authentication password.
        """
        self.email = email
        self.password = password
        self.mega = Mega()
        self.m = None

    def start(self):
        """
        Method responsible for initiating the connection to the mega server.
        """
        try:
            if self.m is None:
                self.m = self.mega.login(self.email, self.password)
                print('Successfully connected to Mega.')
                return True

        except Exception as err:
            print(f'There was an error trying to connect to Mega: {err}')

        return False

    # TODO: compress files before uploading to the cloud.
    def upload_file(self, path_remote: str, file_path: str = None):
        """
        Method responsible for sending the files to the server

        Args:
                path_remote (str): File path
                file (object): Instance of the file object
        """
        try:
            folder = self.__create_directory__(path_remote)

            if folder is None:
                raise Exception('Unable to create or find the folder.')

            # Sleep to avoid any potential timing issues with Mega API
            sleep(2)

            data = self.m.upload(file_path, folder[0])
            # print(f'File uploaded successfully: {data}')

            return True

        except Exception as err:
            print(f'There was a problem: {err}')
            return False

    def download_file(self, file_id: str, file_name, destination_folder: str):
        if not os.path.exists(destination_folder):
            raise Exception('Destination_folder not found')

        file = self.m.find(file_id)
        if file is None:
            raise Exception('File not found')

        self.m.download(file, destination_folder, file_name)

    def __create_directory__(self, directory_name):
        """
        Method to help create remote directories.

        Args:
                directory_name (str): Name that will be given to the directory
                on the server.

        Returns:
                Folder or None if folder couldn't be created.
        """
        try:
            if self.m is None:
                raise Exception('Login required before')

            # Attempt to find the folder
            folder = self.m.find(directory_name, exclude_deleted=True)

            # If the folder doesn't exist, create it
            if folder is None:
                print(f"Folder '{directory_name}' does not exist. Creating it now...")
                folder = self.m.create_folder(directory_name)
                print(f"Folder '{directory_name}' created successfully.")

            return self.m.find(directory_name)

        except Exception as err:
            print(f'Error creating directory: {err}')

        return None
