import os
import secrets
from base64 import b64encode

from api.classlib.filehelp import FileHelp
from config import config


# TODO: Documentation a functions
# TODO: Get files in cloud
# TODO: Optimazer database

DB = config.init_database()
MEGA = config.init_mega()


def add_file():
    try:
        print('Enter the path of the file you want to add.')
        file_path = input('>> ')

        if not os.path.exists(file_path):
            raise FileNotFoundError(f'The file {file_path} not exists')

        print('[+] Generate a file id')
        file_id = FileHelp.gen_file_id()
        file_name = os.path.basename(file_path)

        print(file_name)
        print('[+] Generate a file check Sum')

        file_cksum = FileHelp.cksum(file_path)

        # Avoid duplicate files.
        if DB.fetch(file_name=file_name, file_cksum=file_cksum) is not None:
            print('[!] The file has already been added')

        # Generate a file key and file iv for encryption.
        file_key = b64encode(secrets.token_bytes(32)).decode('utf-8')
        file_iv = b64encode(secrets.token_bytes(16)).decode('utf-8')

        # Insert into database a file metadata.
        DB.insert(file_id, file_name, file_path, file_cksum, file_key, file_iv)

        file_out = os.path.join(config.temp_path, file_id)
        FileHelp.encrypt_file(file_key, file_iv, file_path, file_out)

        print('[!] Uploading files to the cloud')

        MEGA.start()
        MEGA.upload_file('pandora', file_out)

        print('[+] Successfuly to adding a new file.')

    except Exception as err:
        print('Error: ', err)


def cksum_verify(file_path, cksum):
    new_cksum = FileHelp.cksum(file_path)
    return new_cksum == cksum


def get_file():
    try:
        print('Insira o id ou o nome do arquivo que deseja.')
        id = input('>> ')

        data = DB.get_file_by_id_or_name(id=id)

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


def list_files():
    try:
        data = DB.fetch_all()
        for file in data:
            print('\n')
            print('--' * 20)
            print(f'File name: {file[1]}')
            print(f'File id: {file[0]}')
            print(f'File path: {file[2]}')
            print(f'File hash: {file[3]}')
            print('--' * 20)

    except Exception as err:
        print(f'Error {err}]')


def remove_file():
    try:
        os.system('clear')
        print('Enter the ID of the file you want to remove.')

        file_id = input('>> ')
        if DB.remove_by_id_or_name(file_id):
            print('[+] File removed with Successfuly')

        else:
            print('[!] Error to remove file.')

    except Exception as err:
        print('Fail: ', err)


def main():
    print('--' * 20)
    print('\tO que deseja fazer ?')
    print('--' * 20)

    print(
        '1 - Listar arquivos. \n2 - Adicionar um arquivo.',
        '\n3 - Puxar os arquivos  \n4 - Deletar um arquivo\n5 - Get File. \n0 - Sair',
    )

    while True:
        opc = int(input('\n>> '))

        match opc:
            case 1:
                list_files()

            case 2:
                add_file()

            case 3:
                pass

            case 4:
                remove_file()

            case 5:
                get_file()

            case 0:
                break

            case _:
                print('Opcao invalida!')


main()
