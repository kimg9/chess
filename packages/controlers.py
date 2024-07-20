from packages import models
from packages import views

"""
Steps :

- Initiate a new tournament (user input)
- Initiate new players (user input)
- Initiate rounds (view)

(- generate_matches(tournament) on first round of tournament
- ask for results (user input)
- end_round with matches result list
- set_current_round on Tournament to change rounds)
*tournament.number_of_rounds

"""


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
                self.list_players_alphabetically()
                self.player_options_menu()
            case 'Return':
                MenuManager().select_object_menu()

    @classmethod
    def create_new_player(self):
        answers = views.PlayerView.create_player()
        models.Player(
            surname=answers['player_surname'],
            name=answers['player_name'],
            birthday=answers['player_birthday'],
            chess_club_id=answers['player_chess_club_id']
        ).save()

    def list_players_alphabetically():
        sorted_list_of_players = sorted(models.Player.load(), key=lambda d: d['name'])
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
            case 'List all tournaments':
                pass
            case 'Search for name and dates of a tournament':
                pass
            case 'List all players alphabetically from a tournament':
                pass
            case 'List all rounds and matchs of a tournament':
                pass
            case 'Return':
                MenuManager().select_object_menu()

    @classmethod
    def create_tournament(self):
        # TOURNAMENT
        tournament_info = views.TournamentView.create_tournament()
        tournament = models.Tournament(
            name=tournament_info['tournament_name'],
            place=tournament_info['tournament_place'],
            start=tournament_info['tournament_start'],
            end=tournament_info['tournament_end'],
            number_of_rounds=int(tournament_info['tournament_number_of_rounds']),
            current_round=None,
            list_of_rounds=[],
            list_of_players=[],
            description=tournament_info['tournament_description']
        )

        # PLAYERS
        players = models.Player.load()
        tournament_players = views.TournamentView.select_tournament_player(players)
        for tournament_player in tournament_players['select_player_for_tournament']:
            for player in players:
                if int(tournament_player.split()[1]) == player['player_id']:
                    created_player = models.Player(
                        surname=player['surname'],
                        name=player['name'],
                        birthday=player['birthday'],
                        chess_club_id=player['chess_club_id']
                    )
                    tournament.list_of_players.append(created_player)

        # ROUNDS
        rounds = views.RoundView.create_rounds(tournament.number_of_rounds)
        for index, value in enumerate(rounds):
            if value:
                round = models.Round(
                    name=value['round_name'],
                    place=value['tournament_place'],
                    start_datetime=value['tournament_start']
                )
                if index == 0:
                    tournament.current_round = round
                round.set_pairs(tournament)
                round.save()
                tournament.list_of_rounds.append(round)
            else:
                views.RoundView.no_rounds_created()
                self.tournament_options_menu()
        tournament.save()

        # SUCCESS
        views.TournamentView.successful_create_tournament()
        self.tournament_options_menu()


class Application():
    def main():
        MenuManager.select_object_menu()
