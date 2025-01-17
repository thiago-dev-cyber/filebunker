import json
import secrets
import sys 
import os 
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad

sys.path.append(os.environ["ROOT"])

class JsonHelp:
    """
    A class that provides functionality to encrypt and decrypt JSON files,
    as well as create encrypted configuration files using AES encryption.

    Attributes:
        config_file_path (str or None): The path to the encrypted configuration file.
    """
    config_file_path = None

    def __init__(self):
        """
        Initializes the JsonHelp class instance.
        """
        pass

    @staticmethod
    def __encrypt_json(data: bytes, key: bytes, iv: bytes) -> bytes:
        """
        Private method to encrypt data using the AES algorithm in CBC mode.

        Args:
            data (bytes): The data to be encrypted.
            key (bytes): AES encryption key (32 bytes).
            iv (bytes): Initialization vector (IV) for CBC mode (16 bytes).

        Returns:
            bytes: The encrypted data.
        """
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(data, AES.block_size))

    @staticmethod
    def __decrypt_json(file_path: str, password: str):
        """
        Private method to decrypt a JSON file using the AES algorithm in CBC mode.

        Args:
            file_path (str): The path to the encrypted JSON file.
            password (str): The password used for key generation.

        Returns:
            tuple: A tuple containing the salt, IV, key, and the decrypted JSON data as a string.
        """
        with open(file_path, "rb") as r:
            salt = r.read(16)  # The salt used for key generation.
            iv = r.read(16)    # The IV used for AES encryption.
            encrypted_data = b64decode(r.read())  # The encrypted data.

        # Generate the AES key from the password and salt.
        key = JsonHelp.__gen_aes_key_to_password(password, salt)

        # Decrypt the data using the AES algorithm in CBC mode.
        cipher = AES.new(key, AES.MODE_CBC, iv)
        data_decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        # Decode the decrypted data to a string (UTF-8).
        data_decrypted = data_decrypted.decode('utf-8')

        print("Decrypted data:")
        print(data_decrypted)
        return salt, iv, key, data_decrypted

    @classmethod
    def decrypt_file(cls, file_path: str, password: str):
        """
        Public method to decrypt a file using the specified password.

        Args:
            file_path (str): The path to the encrypted JSON file.
            password (str): The password used for decryption.

        Returns:
            tuple: The result of the decryption, including the salt, IV, key, and decrypted data.
        """
        return cls.__decrypt_json(file_path, password)

    @classmethod
    def encrypt_file(cls, data: bytes, key: bytes, iv: bytes):
        """
        Public method to encrypt data using the AES algorithm in CBC mode.

        Args:
            data (bytes): The data to be encrypted.
            key (bytes): The AES encryption key.
            iv (bytes): The initialization vector for CBC mode.

        Returns:
            bytes: The encrypted data.
        """
        return cls.__encrypt_json(data, key, iv)

    @classmethod
    def create_config_file(cls, config_file_name: str = None, password: str = None):
        """
        Creates and writes an encrypted configuration file with AES encryption.

        Args:
            config_file_name (str): The name of the configuration file to be created.
            password (str): The password used to derive the AES key.
        """
        # Generate salt and IV for the encryption process.
        salt = secrets.token_bytes(16)  # Salt for key generation.
        iv = secrets.token_bytes(16)    # Initialization vector (IV).
        
        # Derive the AES key from the password and salt.
        key = JsonHelp.__gen_aes_key_to_password(password, salt)

        # Set the path for the configuration file.
        config_file_path = os.path.join(os.path.join(os.environ["ROOT"], "data"), config_file_name)
        cls.config_file_path = config_file_path

        # Prepare the configuration data.
        data = {
            "json_path": config_file_path,
            "paths": {}
        }

        # Convert the data to JSON and then to bytes.
        data = json.dumps(data, ensure_ascii=False).encode('utf-8')

        # Encrypt the data.
        encrypted_data = b64encode(cls.__encrypt_json(data, key, iv))

        # Write the encrypted data, salt, and IV to the file.
        with open(config_file_path, "wb") as f:
            f.write(salt)  # Write the salt.
            f.write(iv)    # Write the IV.
            f.write(encrypted_data)  # Write the encrypted data.

    @staticmethod
    def __gen_aes_key_to_password(password: str, salt: bytes) -> bytes:
        """
        Generates an AES key from the provided password and salt using PBKDF2.

        Args:
            password (str): The password used for key generation.
            salt (bytes): The salt used in the PBKDF2 function.

        Returns:
            bytes: The derived AES key.
        """
        return PBKDF2(password, salt, dkLen=32, count=1000000)


if __name__ == '__main__':

    # Decrypt the file using the specified password.
    JsonHelp.decrypt_file(file_path='1.json', password="123456")

    import os, inspect
    # Print the absolute path of the current script file.
    print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
