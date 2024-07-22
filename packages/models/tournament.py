from packages.models.round import Round, Match
from packages.models.player import Player
import random
import json


class Tournament():
    def __init__(
                self,
                name,
                place,
                start,
                end,
                current_round: Round,
                list_of_players: list,
                list_of_rounds: list,
                list_of_matches: list,
                description: str,
                number_of_rounds: int,
            ):
        self.name = name
        self.place = place
        self.start = start
        self.end = end
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.list_of_rounds = list_of_rounds
        self.list_of_matches = list_of_matches
        self.list_of_players = list_of_players
        self.description = description

    def ordonate_list_of_players(self):
        if len(self.list_of_rounds) == 1:
            random.shuffle(self.list_of_players)
        else:
            self.list_of_players = sorted(self.list_of_players, key=lambda player: player.score, reverse=True)

    def uneven_number_of_players(self):
        new_match = Match()
        new_match.pair_of_players += (
                [self.list_of_players[-1].player_id, 0],
            )
        self.list_of_matches.append(new_match)

    def save(self):
        with open('data/tournaments/tournament.json', 'r+') as file:
            try:
                tournaments = json.load(file)
            except json.decoder.JSONDecodeError:
                tournaments = []
            tournaments.append(self)
            file.seek(0)
            file.truncate()
            file.write(json.dumps(tournaments, default=lambda o: getattr(o, '__dict__', str(o))))
            file.flush()
            file.close()

    @staticmethod
    def load_into_dict():
        with open('data/tournaments/tournament.json', 'r+') as file:
            try:
                tournaments = json.load(file)
            except json.decoder.JSONDecodeError:
                tournaments = []
        return tournaments

    @staticmethod
    def load_into_obj():
        with open('data/tournaments/tournament.json', 'r+') as file:
            try:
                tournaments = [Tournament(**x) for x in json.load(file)]
            except json.decoder.JSONDecodeError:
                tournaments = []

            if tournaments:
                for tournament in tournaments:
                    temp_players = []
                    temp_matches = []
                    temp_rounds = []
                    for player in tournament.list_of_players:
                        temp_players.append(Player(**player))
                    tournament.list_of_players = temp_players
                    for match in tournament.list_of_matches:
                        temp_matches.append(Match(**match))
                    tournament.list_of_matches = temp_matches
                    for round in tournament.list_of_rounds:
                        temp_rounds.append(Round(**round))
                    tournament.list_of_rounds = temp_rounds
                    tournament.current_round = Round(**tournament.current_round) if tournament.current_round else None
        return tournaments

    def update(self):
        with open('data/tournaments/tournament.json', 'r+') as file:
            tournaments = self.load_into_obj()
            updated_tournaments = []
            if tournaments:
                for tournament in tournaments:
                    if tournament.name == self.name:
                        updated_tournaments.append(self)
                    else:
                        updated_tournaments.append(tournament)
            else:
                updated_tournaments.append(self)
            file.seek(0)
            file.truncate()
            file.write(json.dumps(updated_tournaments, default=lambda o: getattr(o, '__dict__', str(o))))
            file.flush()
            file.close()
