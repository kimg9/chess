import inquirer.errors
import tabulate
import inquirer
import re


def chess_club_id_validation(answers, current):
    if not re.match(r"[A-Z]{2}\d{5}", current):
        reason_string = "Chess club ID must be two characters followed by 5 digits (example: AB12345)."
        raise inquirer.errors.ValidationError("", reason=reason_string)
    return True


def date_validation(answers, current):
    if not re.match(r"\d{2}/\d{2}/\d{4}$", current):
        raise inquirer.errors.ValidationError("", reason="Date must be formatted as DD/MM/YYYY (example: 19/10/1995)")
    return True


def number_validation(answers, current):
    if not re.match(r"\d*$", current):
        raise inquirer.errors.ValidationError("", reason="Must be a number.")
    return True


class MainMenus():
    def select_object():
        print("Welcome in our Chess Tournament App!")
        questions = [
            inquirer.List(
                'select_object',
                message='Please chose one of the following options',
                choices=['Player', 'Tournament', 'Exit']
            )
        ]
        answer = inquirer.prompt(questions)
        return answer


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
                validate=date_validation,
            ),
            inquirer.Text(
                'player_chess_club_id',
                message='What is their chess club id? (format: AB12345)',
                validate=chess_club_id_validation,
            )
        ]
        answer = inquirer.prompt(questions)
        return answer

    def successful_create_player(self):
        print("You successfully created a new player!")
        print("Returning to player menu")

    def list_players_alphabetically(rows, header):
        print(tabulate.tabulate(rows, header))


class TournamentView():
    def select_options_tournament():
        questions = [
            inquirer.List(
                'select_options_tournament',
                message='Please chose one of the following options',
                choices=[
                    'Create new tournament',
                    'List all tournaments',
                    'Search for name and dates of a tournament',
                    'List all players alphabetically from a tournament',
                    'List all rounds and matchs of a tournament',
                    'Return',
                ]
            )
        ]
        answer = inquirer.prompt(questions)
        return answer

    def create_tournament():
        print("Please complete the following information to create your tournament.")
        questions = [
            inquirer.Text(
                'tournament_name',
                message='Name:',
            ),
            inquirer.Text(
                'tournament_place',
                message='Place:',
            ),
            inquirer.Text(
                'tournament_start',
                message='Start date:',
                validate=date_validation,
            ),
            inquirer.Text(
                'tournament_end',
                message='End date:',
                validate=date_validation,
            ),
            inquirer.Text(
                'tournament_number_of_rounds',
                message='Number of rounds:',
                default=4,
                validate=number_validation,
            ),
            inquirer.Text(
                'tournament_description',
                message='Description:',
            ),
        ]
        answer = inquirer.prompt(questions)
        return answer

    def select_tournament_player(players):
        questions = [
            inquirer.Checkbox(
                'select_player_for_tournament',
                message='Please select the players that will participate in this tournament. (Right arrow to select)',
                choices=[
                    "Player %s" %
                    player['player_id'] + " - " +
                    player["name"] + " " +
                    player["surname"]
                    for player in players
                ],
            )
        ]
        answer = inquirer.prompt(questions)
        return answer

    def successful_create_tournament():
        print("You successfully created a new tournament!")
        print("Returning to tournament menu")


class RoundView():
    def create_rounds(number_of_rounds):
        answers = []
        for number in range(number_of_rounds):
            print(f"Please complete the following information for round number {number + 1}.")
            questions = [
                inquirer.Text(
                    'round_name',
                    message='Name:',
                ),
                inquirer.Text(
                    'tournament_place',
                    message='Place:',
                ),
                inquirer.Text(
                    'tournament_start',
                    message='Start date and time:',
                )
            ]
            answers.append(inquirer.prompt(questions))
        return answers

    def no_rounds_created():
        print("Something is wrong, there was no information for rounds. Tournament was not created. Please try again.")
