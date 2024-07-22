import inquirer.errors
import tabulate
import inquirer
from packages.views.main_menu import clear
from packages.views.validations import Validations


class TournamentView():
    """
    A view for rounds
    """
    def select_options_tournament():
        """
        Menu to select one of the seven operations possible for tournaments or return to main menu.
        """
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
        """
        Form to fill out main information about new tournament.
        """
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
        """
        Choice view to select a player from the list given in param.

        :attr players: list of players
        :type players: List[Player]
        """
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
        """
        Simple view to inform user that they have successfully created a new tournament.
        """
        print("You successfully created a new tournament!")
        print("Returning to tournament menu\n")

    def list_tournaments(rows, header):
        """
        View to transform header + rows into a table.

        :attr rows: value for the table
        :type rows: dict_values
        :attr heaader: header for the table
        :type heaader: dict_keys
        """
        print(tabulate.tabulate(rows, header) + "\n")

    def select_tournament(tournaments):
        """
        Choice view to select a tournament from the list given in param.

        :attr tournaments: list of tournaments
        :type tournaments: List[Tournament]
        """
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
