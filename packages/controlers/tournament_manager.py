from packages.views import tournament_view
from packages.views import round_view
from packages.controlers import menu_manager
from packages.controlers import player_manager
from packages.models.tournament import Tournament
from packages.models.player import Player
from packages.models.round import Round

from datetime import datetime


class TournamentManager():
    """
    A class to represent the options contained in the "Tournament" menu
    """
    @classmethod
    def tournament_options_menu(self):
        """
        Redirects the user to the correct methods and views depending on the selected option.
        There are 7 options the user can chose from.
        """
        answer = tournament_view.TournamentView.select_options_tournament()
        match answer['select_options_tournament']:
            case 'Create new tournament':
                self.create_tournament()
                tournament_view.TournamentView.successful_create_tournament()
                self.tournament_options_menu()
            case 'List all tournaments':
                self.list_all_tournaments()
                self.tournament_options_menu()
            case 'Search for name and dates of a tournament':
                self.get_tournaments_by_round()
                self.tournament_options_menu()
            case 'List all players alphabetically from a tournament':
                self.list_players_of_tournaments()
                self.tournament_options_menu()
            case 'List all rounds and matchs of a tournament':
                self.list_rounds_matchs_tournament()
                self.tournament_options_menu()
            case 'Update round scores and create new round':
                self.update_current_round_and_create_new()
                round_view.RoundView.successful_create_round()
                self.tournament_options_menu()
            case 'Return':
                menu_manager.MenuManager().select_object_menu()

    @classmethod
    def create_tournament(self):
        """
        A method to create a new tournament.
        Gives a form to the user to fill.
        Uses the filled information to create a new instance of a Tournament.
        Pass this instance of a tournament to two function:
        - Function create_new_list_of_players to chose the players playing in the tournament.
        - Function create_new_round to generate the first round of the tournament.
        """
        tournament_info = tournament_view.TournamentView.create_tournament()
        tournament = Tournament(
            name=tournament_info['tournament_name'],
            place=tournament_info['tournament_place'],
            start=tournament_info['tournament_start'],
            end=tournament_info['tournament_end'],
            number_of_rounds=int(tournament_info['tournament_number_of_rounds']),
            current_round=None,
            list_of_rounds=[],
            list_of_matches=[],
            list_of_players=[],
            description=tournament_info['tournament_description']
        )
        self.create_new_list_of_players(tournament)
        self.create_new_round(tournament)

    def create_new_list_of_players(tournament: Tournament):
        """
        A method to bind tournament and list of players.
        Loads all the players from the DB.
        Use thoses players to call a view making the user chose the relevant players.
        Append to the tournament param list_of_players the players that were selected.

        :param tournament: an instance of an object Tournament
        :type tournament: Tournament
        """
        players = Player.load_into_obj()
        tournament_players = tournament_view.TournamentView.select_tournament_player(players)
        for tournament_player in tournament_players['select_player_for_tournament']:
            for player in players:
                if int(tournament_player.split()[1]) == player.player_id:
                    tournament.list_of_players.append(player)
        tournament.update()

    def create_new_round(tournament: Tournament):
        """
        A method to create a new round to a tournament.
        It checks if the tournament has reached all its rounds or not.
        If yes : display a view to inform the user that the tournament has enough rounds
        If no : gives the user a view with a form to fill.
        Uses the response to create an instance of a Round object.
        Generate the pairs and matches for this round.
        Save the round in the DB.
        Update the current_round attribute of the tournament.
        Append the list_of_rounds attribute of the tournament
        Update the tournament in the DB.

        :param tournament: an instance of an object Tournament
        :type tournament: Tournament
        """
        if len(tournament.list_of_rounds) != tournament.number_of_rounds:
            rounds = round_view.RoundView.create_rounds()
            round = Round(
                name=rounds['round_name'],
                place=rounds['round_place'],
            )
            round.set_pairs(tournament)
            round.save()
            tournament.current_round = round
            tournament.list_of_rounds.append(round)
            tournament.update()
        else:
            round_view.RoundView.maximum_reached()

    def list_all_tournaments():
        """
        A method to display all tournaments.
        It loads all the Tournaments into a list of dicts.
        For each value, clean the data so that it is easier to read once printed on screen.
        Create header and rows with keys and values and send then to the relevant view.
        """
        list_of_tournaments = Tournament.load_into_dict()
        for tournament in list_of_tournaments:
            tournament["list_of_rounds"] = [value["name"] for value in tournament["list_of_rounds"]]
            tournament["list_of_players"] = [
                value["surname"] + " " + value["name"]
                for value in tournament["list_of_players"]
            ]
            tournament["current_round"] = tournament["current_round"]["name"]
            tournament.pop("list_of_matches")
        header = list_of_tournaments[0].keys()
        rows = [v.values() for v in list_of_tournaments]
        tournament_view.TournamentView.list_tournaments(rows, header)

    def list_players_of_tournaments():
        """
        A method to list all players of a tournament.
        It loads all the Tournaments into a list of dicts.
        Propose a view to the user for them to select a tournament.
        Get all the Players for the selected tournament and order them alphabetically.
        """
        tournaments = Tournament.load_into_dict()
        answer = tournament_view.TournamentView.select_tournament(tournaments)
        for tournament in tournaments:
            if tournament["name"] == answer["select_tournament"][0]:
                player_manager.PlayerManager.list_players_alphabetically(tournament['list_of_players'])
                break

    def list_rounds_matchs_tournament():
        """
        A method to list all rounds and matches of that round for a tournament.
        It loads all the Tournaments into a list of dicts.
        Propose a view to the user for them to select a tournament.
        Get all the rounds for this tournament.
        Create header and rows with keys and values and send then to the relevant view.
        """
        tournaments = Tournament.load_into_dict()
        answer = tournament_view.TournamentView.select_tournament(tournaments)
        for tournament in tournaments:
            if tournament["name"] == answer["select_tournament"][0]:
                round_dict = []
                for round in tournament['list_of_rounds']:
                    round_dict.append(round)
                header = round_dict[0].keys()
                rows = [v.values() for v in round_dict]
                tournament_view.TournamentView.list_tournaments(rows, header)

    def get_tournaments_by_round():
        """
        A method to get a tournament by selecting a round.
        It loads all the rounds in the DB, sends these rounds to a view where the user
        can chose the desired round.
        Then it loads all tournaments, finds the tournament where the selected round is and then returns the tournament
        data polished and with a header and a rows to send to a view.
        """
        rounds = Round.load()
        answer = round_view.RoundView.select_round(rounds)
        tournaments = Tournament.load_into_dict()
        for tournament in tournaments:
            for round in tournament["list_of_rounds"]:
                if answer["select_rounds"][0] == round["name"]:
                    tournament["list_of_rounds"] = [value["name"] for value in tournament["list_of_rounds"]]
                    tournament["list_of_players"] = [
                        value["surname"] + " " + value["name"]
                        for value in tournament["list_of_players"]
                    ]
                    tournament["current_round"] = tournament["current_round"]["name"]
                    tournament.pop("list_of_matches")
                    rows = []
                    rows.append(tournament.values())
                    header = tournaments[0].keys()
                    tournament_view.TournamentView.list_tournaments(rows, header)
                    break
            break

    @classmethod
    def update_current_round_and_create_new(self):
        """
        A method to close a current round and set the scores of the player then create a new round.
        It loads the tournaments from the DB and passes then to a view.
        It then isolates the selected tournament as an object as well as the current round of this tournament
        as a Round object.

        It then checks if it is the last round or not for this specific tournament. If it is, it displays
        a view informing the user. Otherwise, it asks the user for the result of the round.
        It loads all the player and updates their score as well as the score for their match in the round.
        It changes the status for the Round to "is_over", sets an end date and updates the round in the database.
        It updates the round in the tournament object too, then updates the database.
        Then it redirects to the method to create a new round for the tournament.
        """
        tournament_answer = tournament_view.TournamentView.select_tournament(Tournament.load_into_dict())

        selected_tournament = None
        selected_round = None
        tournaments = Tournament.load_into_obj()
        rounds = Round.load()
        for tournament in tournaments:
            if tournament.name == tournament_answer["select_tournament"][0]:
                selected_tournament = tournament
                for round in rounds:
                    if round.round_id == tournament.current_round.round_id:
                        selected_round = round
                        break
            break

        if len(selected_tournament.list_of_rounds) != selected_tournament.number_of_rounds:
            answers = round_view.RoundView.result_of_round(selected_round)

            players = Player.load_into_obj()
            for answer in answers:
                for round_match in selected_round.round_matches:
                    if answer[0] == round_match.match_id:
                        if answer[1]['select_rounds'] == "It's a draw":
                            round_match.pair_of_players[0][1] += 0.5
                            round_match.pair_of_players[1][1] += 0.5
                            for player in players:
                                if player.player_id == round_match.pair_of_players[0][0]:
                                    player.score += 0.5
                                    player.update()
                                elif player.player_id == round_match.pair_of_players[1][0]:
                                    player.score += 0.5
                                    player.update()
                        elif int(answer[1]['select_rounds'].split()[1]) == round_match.pair_of_players[0][0]:
                            round_match.pair_of_players[0][1] += 1
                            for player in players:
                                if player.player_id == round_match.pair_of_players[0][0]:
                                    player.score += 1
                                    player.update()
                        elif int(answer[1]['select_rounds'].split()[1]) == round_match.pair_of_players[1][0]:
                            round_match.pair_of_players[1][1] += 1
                            for player in players:
                                if player.player_id == round_match.pair_of_players[1][0]:
                                    player.score += 1
                                    player.update()
            selected_round.is_over = "Yes"
            selected_round.end_datetime = datetime.now()
            selected_round.update()

            for index, round in enumerate(selected_tournament.list_of_rounds):
                if int(round.round_id) == selected_round.round_id:
                    selected_tournament.list_of_rounds.pop(index)
                    selected_tournament.list_of_rounds.insert(index, selected_round)
            selected_tournament.update()

            round_view.RoundView.successful_update_round()
            self.create_new_round(selected_tournament)
        else:
            round_view.RoundView.maximum_reached()
