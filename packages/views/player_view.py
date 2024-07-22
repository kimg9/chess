import inquirer.errors
import tabulate
import inquirer
from packages.views.main_menu import clear
from packages.views.validations import Validations


class PlayerView():
    @staticmethod
    def select_options_player():
        questions = [
            inquirer.List(
                'select_options_player',
                message='Please chose one of the following options',
                choices=[
                    'Create new player',
                    'List all players in alphabetical order',
                    'Return',
                ]
            )
        ]
        answer = inquirer.prompt(questions)
        clear()
        return answer

    def create_player():
        questions = [
            inquirer.Text(
                'player_surname',
                message='What is their surname?',
            ),
            inquirer.Text(
                'player_name',
                message='What is their name?',
            ),
            inquirer.Text(
                'player_birthday',
                message='What is their birthday? (format: DD/MM/YY)',
                validate=Validations.date_validation,
            ),
            inquirer.Text(
                'player_chess_club_id',
                message='What is their chess club id? (format: AB12345)',
                validate=Validations.chess_club_id_validation,
            )
        ]
        answer = inquirer.prompt(questions)
        clear()
        return answer

    def successful_create_player(self):
        print("You successfully created a new player!")
        print("Returning to player menu \n")

    def list_players_alphabetically(rows, header):
        print(tabulate.tabulate(rows, header) + "\n")
