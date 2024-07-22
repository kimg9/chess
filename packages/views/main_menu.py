import inquirer
from os import system, name


def clear():
    """
    Function to clear the window in the terminal.
    """
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


class MainMenus():
    """
    A view for the main menu.
    """
    def select_object():
        """
        View linked to the MainMenu in the menu manager.
        Displays the 3 initial choices for the user.
        """
        print("Welcome in our Chess Tournament App!")
        questions = [
            inquirer.List(
                'select_object',
                message='Please chose one of the following options',
                choices=['Player', 'Tournament', 'Exit']
            )
        ]
        answer = inquirer.prompt(questions)
        clear()
        return answer
