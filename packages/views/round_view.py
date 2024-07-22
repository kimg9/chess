import inquirer.errors
import inquirer
from packages.views.main_menu import clear


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
