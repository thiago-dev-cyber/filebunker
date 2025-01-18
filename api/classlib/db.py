import json
import os
import sys
import traceback
from base64 import b64encode


# Adds the root directory to the Python search path.
sys.path.append(os.environ['ROOT'])

from api.classlib.jsonhelp import JsonHelp


class DataBase:
    """
    A class that handles the saving, loading, and encryption
    of JSON data to/from a file.

    This class abstracts the handling of JSON data, providing 
    methods to save and load the data to a file, including 
    encryption and decryption functionalities.
    """

    def __init__(self, json_data: dict, salt: bytes, iv: bytes, key: bytes):
        """
        Inicialization object.

        Args:
            json_file (dict): Extracted json information.
            salt (bytes): The salt password.
            iv (bytes): The vector of inicialization.

        Returns:
            None

        """
        # Ensuring that the JSON file is converted correctly.
        self.db = json.loads(json_data) if isinstance(json_data, str) else json_data
        self.salt = salt
        self.iv = iv
        self.key = key

    def save(self):
        """
        method responsible for persisting the information in the.
        """
        try:
            print(self.db)
            # Re-converting the dictionary to json and serializing into bytes.
            data = json.dumps(self.db, ensure_ascii=False).encode('utf-8')
            encrypted_data = JsonHelp.encrypt_file(data, self.key, self.iv)

            # Saving the encrypted data.
            with open(self.db['json_path'], 'wb') as f:
                f.write(self.salt)
                f.write(self.iv)
                f.write(b64encode(encrypted_data))

        except Exception as err:
            print(
                'An error occurred while saving the information to the file:\n',
                f'{self.db["json_path"]}\nError: {err}'
            )
            traceback.format_exc()
