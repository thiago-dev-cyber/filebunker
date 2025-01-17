import os
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from os import urandom
import base64


class FileHelp:
    """
    A helper class for performing file-related operations such as checksum generation, 
    encryption, and decryption using AES algorithm.
    """

    @staticmethod
    def cksum(path):
        """
        Computes the MD5 checksum of the given file.

        Args:
            path (str): The path to the file.

        Returns:
            str: The MD5 checksum of the file in hexadecimal format. If the file does not exist or 
                 is a symbolic link, an empty string is returned.
        """
        if os.path.exists(path):
            if os.path.islink(path):
                # Resolve symbolic link to get the actual file path
                path = os.path.realpath(path)
            
            with open(path, 'rb') as file:
                file_hash = hashlib.md5()
                # Reading the file in chunks to avoid memory overload on large files
                while chunk := file.read(8192):
                    file_hash.update(chunk)
                    
                return file_hash.hexdigest()
        
        return ""

    @staticmethod
    def encrypt_file(key, iv, in_filename, out_filename, chunk_size=64*1024):
        """
        Encrypts a file using AES encryption (CBC mode).

        Args:
            key (bytes): The encryption key (must be 16, 24, or 32 bytes in length).
            iv (bytes): The initialization vector for AES encryption (must be 16 bytes).
            in_filename (str): Path to the input (unencrypted) file.
            out_filename (str): Path to the output (encrypted) file.
            chunk_size (int): The size of the chunks to be read and encrypted. Default is 64KB.
        """
        try:
            # Create a new AES encryptor object with the given key, IV, and mode
            encryptor = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
            file_size = os.path.getsize(in_filename)

            if file_size < chunk_size:
                chunk_size = file_size

            with open(in_filename, "rb") as infile:
                with open(out_filename, "wb") as outfile:

                    while True:
                        # Read the file in chunks to avoid memory overload
                        file_chunk = infile.read(chunk_size)

                        if len(file_chunk) == 0:
                            break

                        # If the chunk length is not a multiple of 16, pad it
                        if len(file_chunk) % 16 != 0:
                            file_chunk = pad(file_chunk, AES.block_size)

                        # Encrypt the chunk and write it to the output file
                        outfile.write(encryptor.encrypt(file_chunk))

        except Exception as err:
            print(f"Error during encryption of file {in_filename}: {err}")

    @staticmethod
    def decrypt_file(key, iv, in_filename, out_filename, chunk_size=64*1024):
        """
        Decrypts a file that was encrypted with AES encryption (CBC mode).

        Args:
            key (bytes): The decryption key (must match the encryption key).
            iv (bytes): The initialization vector used during encryption (must match the IV).
            in_filename (str): Path to the input (encrypted) file.
            out_filename (str): Path to the output (decrypted) file.
            chunk_size (int): The size of the chunks to be read and decrypted. Default is 64KB.
        """
        try:
            # Create a new AES decryptor object with the given key, IV, and mode
            decryptor = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
            file_size = os.path.getsize(in_filename)

            if file_size < chunk_size:
                chunk_size = file_size

            with open(in_filename, "rb") as infile:
                with open(out_filename, "wb") as outfile:

                    while True:
                        # Read the file in chunks
                        file_chunk = infile.read(chunk_size)

                        if len(file_chunk) == 0:
                            break

                        # Decrypt the chunk
                        decrypt_chunk = decryptor.decrypt(file_chunk)

                        # If it's the last chunk, remove padding
                        if len(file_chunk) == file_size % chunk_size:
                            decrypt_chunk = unpad(decrypt_chunk, AES.block_size)

                        # Write the decrypted chunk to the output file
                        outfile.write(decrypt_chunk)

        except Exception as err:
            print(f"Error during decryption of file {in_filename}: {err}")

