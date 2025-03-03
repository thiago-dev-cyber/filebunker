# Defaults methods
import os
import secrets
from base64 import b64encode

# External methods
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor, as_completed

# Local methods
from api.classlib.filehelp import FileHelp
from config import config


DB = config.init_database()
MEGA = config.init_mega()


def add_file(file_path):
    """Adds a new file to the database and uploads it to the cloud."""
    try:
        file_path = file_path
        file_id = FileHelp.gen_file_id()
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        
        file_cksum = FileHelp.cksum(file_path)

        if DB.fetch(file_name=file_name, file_cksum=file_cksum):
            print('[!] The file has already been added')
            return

        file_key = b64encode(secrets.token_bytes(32)).decode('utf-8')
        file_iv = b64encode(secrets.token_bytes(16)).decode('utf-8')

        DB.insert(file_id, file_name, file_path, file_cksum, file_key, file_iv, file_size)

        file_out = os.path.join(config.temp_path, file_id)
        FileHelp.encrypt_file(file_key, file_iv, file_path, file_out)

        print('[!] Uploading files to the cloud...')
        MEGA.start()
        MEGA.upload_file('filebunker', file_out)

        print('[+] File added successfully.')

    except Exception as err:
        print('Error:', err)


def add_directory():
    try:
        directory_path = get_input('Enter the path of the directory you want to add: ', validate_dir_exists)

        with ThreadPoolExecutor(max_workers=5) as executor:  # Limite de 5 threads
            futures = []

            for root, dirs, files in os.walk(directory_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    futures.append(executor.submit(add_file, file_path=file_path))

            # Aguardar a execução de todas as threads
            for future in as_completed(futures):
                try:
                    future.result()  # Pode lançar exceções que ocorrem na thread
                    print("[+] Successfully processed a file.")
                except Exception as e:
                    print(f"[!] Error processing file: {e}")
                    
    except Exception as err:
        print('Error:', err)


# TODO: 
def download_directory():
    try:
        directory_path = get_input('Enter the path of the directory ')
    except Exception as err:
        print('Error: ', err)

def get_input(prompt, validate_func=None):
    """Helper function to get validated user input."""
    while True:
        user_input = input(f'{prompt}\n>> ')
        if validate_func and not validate_func(user_input):
            print('[!] Invalid input, please try again.')
        else:
            return user_input


def validate_file_exists(file_path):
    """Validates that the file exists."""
    return os.path.exists(file_path)


def validate_dir_exists(dir_path):
    """Validates that the directory exists"""
    return os.path.isdir(dir_path)


#def list_files():
    """Lists all files stored in the database."""
#    try:
#        data = DB.fetch_all()
#        for file in data:
#            print(f"\n{'--' * 20}\nFile name: {file[1]}\nFile id: {file[0]}\nFile path: {file[2]}\nFile hash: {file[3]}\n{'--' * 20}")
#    except Exception as err:
#        print(f'Error: {err}')

def list_files():
    """Lists all files stored in the database in a formatted table."""

    while True:
        try:
            data = DB.fetch_all()
            
            # Format the data for tabulation
            table_data = []
            for file in data:
                table_data.append([file[0], 
                    file[1], 
                    file[2], 
                    file[3], 
                    FileHelp.parser_bytes(int(file[6]))])

            # Define column headers
            headers = ['File ID', 'File Name', 'File Path', 'File Hash', 'File Size']

            # Print the table using tabulate
            print(tabulate(table_data, headers, tablefmt='fancy_grid'))

            if not get_input("Deseja exibir mais 10 ?").lower() in ["y", "yes"]:
                break

        except Exception as err:
            print(f'Error: {err}')


def remove_file():
    """Removes a file by its ID or name."""
    try:
        file_id = get_input('Enter the ID of the file you want to remove: ')
        if DB.remove_by_id_or_name(file_id):
            print('[+] File removed successfully')
        else:
            print('[!] Error removing file.')
    except Exception as err:
        print('Error:', err)



def cksum_verify(file_path, cksum):
    new_cksum = FileHelp.cksum(file_path)
    return new_cksum == cksum


def get_file():
    try:
        file_id = get_input('Enter the path of file: ')

        data = DB.get_file_by_id_or_name(id=file_id)

        # TODO: Get file in cloud
        if data[0] not in os.listdir(config.temp_path):
            print('[*] Getting file in clound.')
            MEGA.start()
            MEGA.download_file(data[0], data[0], config.temp_path)

        current = os.path.join(config.temp_path, data[0])

        FileHelp.decrypt_file(data[4], data[5], current, data[2])
        print(cksum_verify(data[2], data[3]))

    except Exception as err:
        print('Erro ', err)



def main():
    """Main menu and program loop."""
    menu = '''
    1 - List files
    2 - Add a file
    3 - Add directory
    4 - Pull files (cloud sync)
    5 - Remove a file
    6 - Get file
    0 - Exit
    '''

    while True:
        print(menu)
        option = int(input('Choose an option: '))

        if option == 1:
            list_files()

        elif option == 2:
            file_path = get_input('Enter the path of the file you want to add: ', validate_file_exists)
            add_file(file_path)
        elif option == 3:
            add_directory() 

        elif option == 4:
            pass

        elif option == 5:
            remove_file()

        elif option == 6:
            get_file()  # Define this function if needed
        elif option == 0:
            break
        else:
            print('[!] Invalid option.')


if __name__ == '__main__':
    main()
