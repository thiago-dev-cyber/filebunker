import inspect
import os
import sys
from getpass import getpass
from time import sleep

from dotenv import load_dotenv


load_dotenv()

# Get the ROOT directory
CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ROOT = os.path.dirname(os.path.dirname(CURRENTDIR))

# Adding the ROOT directory to sys.path
sys.path.append(ROOT)
os.environ['ROOT'] = ROOT

from api.classlib.connect_mega import ConnectMega
from api.classlib.manager import Manager
from api.classlib.menu import Menu
from api.classlib.jsonhelp import JsonHelp


def clear_screen():
    """Clears the terminal screen."""
    os.system('clear || cls')


def animation():
    """Displays the animated loading sequence."""
    animations = [
        Menu.anim_01,
        Menu.anim_02,
        Menu.anim_03,
        Menu.anim_04,
        Menu.anim_05,
    ]

    for anim in animations:
        clear_screen()
        print(anim)
        sleep(1.50)


def prompt_menu(menu_text, options):
    """
    Displays a menu and prompts the user for input.

    Args:
        menu_text (str): The text to display for the menu.
        options (list[int]): List of valid options.

    Returns:
        int: The selected option.
    """
    while True:
        try:
            clear_screen()
            print(menu_text)
            choice = int(input('>> '))
            print(choice)
            if choice in options:
                return choice
            print(f'Invalid option! Please select one of {options}.')
        except ValueError:
            print('Invalid input! Please enter a number.')

        except KeyboardInterrupt:
            print('\nExiting...')
            sys.exit()


def main_menu(m):
    """
    Displays the main menu and handles file upload/download operations.

    Args:
        m (ConnectMega): The Mega connection object.
    """
    Manager.reload_files_pool()

    while True:
        choice = prompt_menu(Menu.main_menu, [1, 2, 3, 0])

        if choice == 1:
            print('Uploading files...')
            Manager.upload_files(m)

        elif choice == 2: 
            print('Downloading files...')
            sleep(5)
            Manager.download_files(m)

        elif choice == 3:
            print("Enter the new path.")
            path = input('\n>> ')

            Manager.add_path(path)
           
        elif choice == 0:
            print('Returning to the main menu...')
            break


def configure_and_start():
    """
    Prompts the user to configure and start the application.
    """
    print('Enter the path to the configuration file:')
    path = input('>> ').strip()
    print('\nEnter the password:')
    password = getpass('>> ')

    clear_screen()
    print('Loading configuration file...')
    sleep(1)

    if not Manager.init_database(path, password):
        print('Failed to initialize the database. Please check your inputs.')
        sleep(2)
        return

    email = os.getenv('email')
    password = os.getenv('password')

    m = ConnectMega(email, password)
    m.start()

    main_menu(m)



def create_config_file():
    """
    Create a configuration file.
    """
    print('\nEnter the filename: ')
    name = input('>> ')

    print('Enter the file password.')
    password = getpass('>> ')

    JsonHelp.create_config_file(name, password)

    print("[+] Configuration file created successfully")
    sleep(2)


def main():
    """Main entry point for the program."""
    # Uncomment below line to enable animation
    #animation()

    while True:
        choice = prompt_menu(Menu.first_menu, [0, 1, 2])

        if choice == 0:
            print('Exiting the program...')
            break

        elif choice == 1:
            configure_and_start()

        elif choice == 2:
            create_config_file()


if __name__ == '__main__':
    main()
