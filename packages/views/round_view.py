import inquirer.errors
import inquirer
from packages.views.main_menu import clear


class RoundView():
    """
    A view for rounds
    """
    def create_rounds():
        """
        Form to fill out main information about new round.
        """
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
        """
        Simple view to inform user that they have not filled correctly the round form.
        """
        print("There was no information for round. Tournament was not created. Please try again.\n")

    def successful_create_round():
        """
        Simple view to inform user that they have successfully created a new round.
        """
        print("You successfully created a new round!")
        print("Returning to tournament menu \n")

    def successful_update_round():
        """
        Simple view to inform user that they have successfully updated the new round.
        """
        print("\nYou successfully updated current round.\n")

    def maximum_reached():
        """
        Simple view to inform user that all rounds are over for this tournament.
        """
        print("All rounds are over for this tournament. Returning to tournament menu.\n")

    def select_round(rounds):
        """
        Choice view to select a rounds from the list given in param.

        :attr rounds: list of rounds
        :type rounds: List[Round]
        """
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
        """
        Choice view to select a winner for a given round.

        :attr selected_rouns: a round
        :type selected_rouns: Round
        """
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
