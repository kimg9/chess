from packages import models
from packages import views

from datetime import datetime


class MenuManager():
    @staticmethod
    def select_object_menu():
        answer = views.MainMenus.select_object()
        match answer['select_object']:
            case 'Player':
                PlayerManager.player_options_menu()
            case 'Tournament':
                TournamentManager.tournament_options_menu()
            case 'Exit':
                exit()


class PlayerManager():
    @classmethod
    def player_options_menu(self):
        answer = views.PlayerView.select_options_player()
        match answer['select_options_player']:
            case 'Create new player':
                self.create_new_player()
                player_view = views.PlayerView()
                player_view.successful_create_player()
                self.player_options_menu()
            case 'List all players in alphabetical order':
                self.list_players_alphabetically(models.Player.load_into_dict())
                self.player_options_menu()
            case 'Return':
                MenuManager().select_object_menu()

    @classmethod
    def create_new_player(self):
        answers = views.PlayerView.create_player()
        player = models.Player(
            player_id=0,
            surname=answers['player_surname'],
            name=answers['player_name'],
            birthday=answers['player_birthday'],
            chess_club_id=answers['player_chess_club_id']
        )
        player.set_player_id()
        player.save()

    def list_players_alphabetically(players):
        sorted_list_of_players = sorted(players, key=lambda d: d['name'])
        header = sorted_list_of_players[0].keys()
        rows = [v.values() for v in sorted_list_of_players]
        views.PlayerView.list_players_alphabetically(rows, header)


class TournamentManager():
    @classmethod
    def tournament_options_menu(self):
        answer = views.TournamentView.select_options_tournament()
        match answer['select_options_tournament']:
            case 'Create new tournament':
                self.create_tournament()
                views.TournamentView.successful_create_tournament()
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
                views.RoundView.successful_create_round()
                self.tournament_options_menu()
            case 'Return':
                MenuManager().select_object_menu()

    @classmethod
    def create_tournament(self):
        tournament_info = views.TournamentView.create_tournament()
        tournament = models.Tournament(
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
        self.create_new_round(tournament)
        self.create_new_list_of_players(tournament)

    def create_new_list_of_players(tournament):
        players = models.Player.load_into_obj()
        tournament_players = views.TournamentView.select_tournament_player(players)
        for tournament_player in tournament_players['select_player_for_tournament']:
            for player in players:
                if int(tournament_player.split()[1]) == player.player_id:
                    tournament.list_of_players.append(player)

    def create_new_round(tournament: models.Tournament):
        if len(tournament.list_of_rounds) != tournament.number_of_rounds:
            rounds = views.RoundView.create_rounds()
            round = models.Round(
                name=rounds['round_name'],
                place=rounds['round_place'],
            )
            tournament.current_round = round
            round.set_pairs(tournament)
            round.save()
            tournament.list_of_rounds.append(round)
            tournament.update()
        else:
            views.RoundView.maximum_reached()

    def list_all_tournaments():
        list_of_tournaments = models.Tournament.load_into_dict()
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
        views.TournamentView.list_tournaments(rows, header)

    def list_players_of_tournaments():
        tournaments = models.Tournament.load_into_dict()
        answer = views.TournamentView.select_tournament(tournaments)
        for tournament in tournaments:
            if tournament["name"] == answer["select_tournament"][0]:
                PlayerManager.list_players_alphabetically(tournament['list_of_players'])
                break

    def list_rounds_matchs_tournament():
        tournaments = models.Tournament.load_into_dict()
        answer = views.TournamentView.select_tournament(tournaments)
        for tournament in tournaments:
            if tournament["name"] == answer["select_tournament"][0]:
                round_dict = []
                for round in tournament['list_of_rounds']:
                    round_dict.append(round)
                header = round_dict[0].keys()
                rows = [v.values() for v in round_dict]
                views.TournamentView.list_tournaments(rows, header)

    def get_tournaments_by_round():
        rounds = models.Round.load()
        answer = views.RoundView.select_round(rounds)
        tournaments = models.Tournament.load_into_dict()
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
                    views.TournamentView.list_tournaments(rows, header)
                    break
            break

    @classmethod
    def update_current_round_and_create_new(self):
        tournament_answer = views.TournamentView.select_tournament(models.Tournament.load_into_dict())

        selected_tournament = None
        selected_round = None
        tournaments = models.Tournament.load_into_obj()
        rounds = models.Round.load()
        for tournament in tournaments:
            if tournament.name == tournament_answer["select_tournament"][0]:
                selected_tournament = tournament
                for round in rounds:
                    if round.round_id == tournament.current_round.round_id:
                        selected_round = round
                        break
            break

        if len(selected_tournament.list_of_rounds) != selected_tournament.number_of_rounds:
            answers = views.RoundView.result_of_round(selected_round)

            players = models.Player.load_into_obj()
            for answer in answers:
                for round_match in selected_round.round_matches:
                    if answer[0] == round_match.match_id:
                        if answer[1]['select_rounds'] == "It's a draw":
                            round_match.pair_of_players[0][1] += 0.5
                            round_match.pair_of_players[1][1] += 0.5
                            for player in players:
                                if player.player_id == round_match.pair_of_players[0][0]:
                                    player.score += 1
                                    player.update()
                                elif player.player_id == round_match.pair_of_players[1][0]:
                                    player.score += 1
                                    player.update()
                        elif int(answer[1]['select_rounds'].split()[1]) == round_match.pair_of_players[0][0]:
                            round_match.pair_of_players[0][1] += 1
                            for player in players:
                                if player.player_id == round_match.pair_of_players[0][0]:
                                    player.score += 2
                                    player.update()
                        elif int(answer[1]['select_rounds'].split()[1]) == round_match.pair_of_players[1][0]:
                            round_match.pair_of_players[1][1] += 1
                            for player in players:
                                if player.player_id == round_match.pair_of_players[1][0]:
                                    player.score += 2
                                    player.update()
            selected_round.is_over = True
            selected_round.end_datetime = datetime.now()
            selected_round.update()
            views.RoundView.successful_update_round()
            self.create_new_round(selected_tournament)
        else:
            views.RoundView.maximum_reached()


class Application():
    def main():
        MenuManager.select_object_menu()
