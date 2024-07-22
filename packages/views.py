import inquirer.errors
import tabulate
import inquirer
import re
from os import system, name


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


class Validations():
    def chess_club_id_validation(answers, current):
        if not re.match(r"^[A-Z]{2}\d{5}$", current):
            reason_string = "Chess club ID must be two characters followed by 5 digits (example: AB12345)."
            raise inquirer.errors.ValidationError("", reason=reason_string)
        return True

    def date_validation(answers, current):
        if not re.match(r"^(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[012])\/((19|20)\d\d)$", current):
            raise inquirer.errors.ValidationError("", reason="Date must be formatted as DD/MM/YYYY (ex: 19/10/1995)")
        return True

    def number_validation(answers, current):
        if not re.match(r"^\d*$", current):
            raise inquirer.errors.ValidationError("", reason="Must be a number.")
        return True

    def time_validation(answers, current):
        if not re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", current):
            raise inquirer.errors.ValidationError("", reason="Time must be formatted as HH:MM (ex: 12:00)")
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
        clear()
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


class TournamentView():
    def select_options_tournament():
        questions = [
            inquirer.List(
                'select_options_tournament',
                message='Please chose one of the following options',
                choices=[
                    'Create new tournament',
                    'Update round scores and create new round',
                    'List all tournaments',
                    'Search for name and dates of a tournament',
                    'List all players alphabetically from a tournament',
                    'List all rounds and matchs of a tournament',
                    'Return',
                ]
            )
        ]
        answer = inquirer.prompt(questions)
        clear()
        return answer

    def create_tournament():
        print("Please complete the following information to create your tournament.")
        questions = [
            inquirer.Text(
                'tournament_name',
                message='Name',
            ),
            inquirer.Text(
                'tournament_place',
                message='Place',
            ),
            inquirer.Text(
                'tournament_start',
                message='Start date',
                validate=Validations.date_validation,
            ),
            inquirer.Text(
                'tournament_end',
                message='End date',
                validate=Validations.date_validation,
            ),
            inquirer.Text(
                'tournament_number_of_rounds',
                message='Number of rounds',
                default=4,
                validate=Validations.number_validation,
            ),
            inquirer.Text(
                'tournament_description',
                message='Description',
            ),
        ]
        answer = inquirer.prompt(questions)
        clear()
        return answer

    def select_tournament_player(players):
        questions = [
            inquirer.Checkbox(
                'select_player_for_tournament',
                message='Please select the players that will participate in this tournament. (Right arrow to select)',
                choices=[
                    "Player %s" %
                    player.player_id + " - " +
                    player.name + " " +
                    player.surname
                    for player in players
                ],
            )
        ]
        answer = inquirer.prompt(questions)
        clear()
        return answer

    def successful_create_tournament():
        print("You successfully created a new tournament!")
        print("Returning to tournament menu\n")

    def list_tournaments(rows, header):
        print(tabulate.tabulate(rows, header) + "\n")

    def select_tournament(tournaments):
        questions = [
            inquirer.Checkbox(
                'select_tournament',
                message='Please select the tournament. (Right arrow to select)',
                choices=[
                    "%s" %
                    tournament["name"]
                    for tournament in tournaments
                ],
            )
        ]
        answer = inquirer.prompt(questions)
        clear()
        return answer


class RoundView():
    def create_rounds():
        answers = []
        print("Please complete the following information to create a new round:")
        questions = [
            inquirer.Text(
                'round_name',
                message='Name',
            ),
            inquirer.Text(
                'round_place',
                message='Place',
            ),
        ]
        answers.append(inquirer.prompt(questions))
        clear()
        return answers[0]

    def no_rounds_created():
        print("There was no information for round. Tournament was not created. Please try again.\n")

    def successful_create_round():
        print("You successfully created a new round!")
        print("Returning to tournament menu \n")

    def successful_update_round():
        print("\nYou successfully updated current round.\n")

    def maximum_reached():
        print("All rounds are over for this tournament. Returning to tournament menu.\n")

    def select_round(rounds):
        questions = [
            inquirer.Checkbox(
                'select_rounds',
                message='Please select the round. (Right arrow to select)',
                choices=[
                    "%s" %
                    round.name
                    for round in rounds
                ],
            )
        ]
        answer = inquirer.prompt(questions)
        clear()
        return answer

    def result_of_round(selected_round):
        answers = []
        for round_match in selected_round.round_matches:
            questions = [
                inquirer.List(
                    'select_rounds',
                    message=f'Who won match number {round_match.match_id} for round number {selected_round.round_id}?\
                        (Right arrow to select)',
                    choices=[
                        "Player %s" % round_match.pair_of_players[0][0],
                        "Player %s" % round_match.pair_of_players[1][0],
                        "It's a draw"
                    ],
                )
            ]
            answers.append((round_match.match_id, inquirer.prompt(questions)))
        clear()
        return answers
