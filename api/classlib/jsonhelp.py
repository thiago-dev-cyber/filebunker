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
    config_file_path = None

    def __init__(self):
        pass


    @staticmethod
    def __encrypt_json(data: bytes, key: bytes, iv: bytes) -> bytes:

        cipher = AES.new(key, AES.MODE_CBC, iv)
        return cipher.encrypt(pad(data, AES.block_size))


    @staticmethod
    def __decrypt_json(file_path, password):

        with open(file_path, "rb") as r:
            salt = r.read(16) 
            iv = r.read(16)  
            encrypted_data = b64decode(r.read()) 


        key = JsonHelp.__gen_aes_key_to_password(password, salt)

       
        cipher = AES.new(key, AES.MODE_CBC, iv)

        
        data_decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        
        data_decrypted = data_decrypted.decode('utf-8')

        print("Dados descriptografados")
        print(data_decrypted)
        return salt, iv, key, data_decrypted

    @classmethod
    def decrypt_file(cls, file_path, password):

        return cls.__decrypt_json(file_path, password)


    @classmethod
    def encrypt_file(cls, data:bytes, key:bytes, iv:bytes):
        return cls.__encrypt_json(data, key, iv)


    @classmethod
    def create_config_file(cls, config_file_name=None, password=None):

        salt = secrets.token_bytes(16)  
        iv = secrets.token_bytes(16)   
        key = JsonHelp.__gen_aes_key_to_password(password, salt)

        config_file_path = os.path.join(os.path.join(os.environ["ROOT"], "data"), config_file_name)
        cls.config_file_path = config_file_path
        
        data = {
            "json_path":config_file_path,
            "paths": {}
        }

        # Converter dados para JSON e depois para bytes
        data = json.dumps(data, ensure_ascii=False).encode('utf-8')

        # Criptografar os dados
        encrypted_data = b64encode(cls.__encrypt_json(data, key, iv))

        
        with open(config_file_path, "wb") as f:
            f.write(salt)  
            f.write(iv)    
            f.write(encrypted_data) 

    @staticmethod
    def __gen_aes_key_to_password(password: str, salt: bytes):

        return PBKDF2(password, salt, dkLen=32, count=1000000)


if __name__ == '__main__':

    # Descriptografar o arquivo
    JsonHelp.decrypt_file(file_path='1.json', password="123456")

    import os, inspect
  # print(os.environ["ROOT"])
    print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))