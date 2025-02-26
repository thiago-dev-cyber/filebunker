import json
import os

from termcolor import colored

from api.classlib.connect_mega import ConnectMega
from api.classlib.db import DataBase

import mysql.connector 
from mysql.connector import errorcode

class Config:
    def __init__(self):
        self.root = os.path.dirname(__file__)
        self.config_file = os.path.join(self.root, 'configs', 'config.json')
        self.temp_path = os.path.join(self.root, 'data', 'temp')
        self.load_configs()
        self.create_directories()

    def load_configs(self):
        """Loads the configuration from the JSON file."""
        try:
            with open(self.config_file, 'r') as file:
                self.config_data = json.load(file)

        except FileNotFoundError:
            print(colored(f'[!] Configuration file {self.config_file} not found.', 'red'))
            self.config_data = {}

        except json.JSONDecodeError:
            print(colored(f'[!] Failed to parse JSON from {self.config_file}.', 'red'))
            self.config_data = {}

    def get_db_config(self):
        """Returns the database configuration."""
        return self.config_data.get('database', {})

    def get_mega_config(self):
        """Returns the Mega service configuration."""
        return self.config_data.get('services', {}).get('mega', {})

    def get_telegram_config(self):
        """Returns the Telegram service configuration."""
        return self.config_data.get('services', {}).get('telegram', {})

    def init_database(self):
        """Initializes the database if it doesn't exist."""
        db_configs = self.get_db_config()

        host = db_configs.get('host', 'localhost')
        user = db_configs.get('user', 'filebunker')
        port= db_configs.get('port', 3306)
        password = db_configs.get('password', '')
        database = db_configs.get('database', 'metadata')

        try:
            #print(f"Conectando ao banco de dados: {database} em {host}:{port} com usuário {user}")
            conn = mysql.connector.connect(
                host=host,
                user=user,
                port=port,
                password=password,
                database=database
            )
            conn.close()

            print(colored("[+] Successful connection to the database!", "green"))

        except  mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                print(colored(f"[!] Database '{database}' not found. Creating...", "yellow"))

                try:
                    conn = mysql.connector.connect(
                    host=host,
                    user=user,
                    port=port,
                    password=password,
                    )
                    cursor = conn.cursor()
                    cursor.execute(f"CREATE DATABASE {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
                    conn.close()

                except mysql.connector.Error as db_err:
                    if db_err.errno == errorcode.ER_DB_CREATE_EXISTS:
                        print(colored(f"[⁺] The Database {database} Already exists!", "green"))

                    else:
                        print(colored(f"[!] Error creating the database {database}","red"))

        

        else:

            return DataBase(
                host=host,
                user=user,
                port=port,
                password=password,
                database=database
            )  # Return the database instance


    def init_mega(self):
        mega_configs = self.get_mega_config()

        if not mega_configs.get('enabled', False):
            print(colored('[!] Mega services not enabled', 'red'))
            exit(1)

        email = mega_configs['email']
        password = mega_configs['password']

        mega = ConnectMega(email, password)
        return mega

    # TODO: Create an init for telegram
    def init_telegram(self):
        pass

    def create_directories(self):
        """Ensures necessary directories are created."""
        # Create the temp directory
        os.makedirs(self.temp_path, exist_ok=True)
        print(colored('[+] Temp directory created.', 'green'))


# Global instance of the config to be accessed throughout the system
config = Config()
print(config.init_database())