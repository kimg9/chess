from datetime import datetime
from typing import List
import itertools
import random
import json


class Player():
    def __init__(self, surname, name, birthday, chess_club_id, player_id, score=0):
        self.surname = surname
        self.name = name
        self.birthday = birthday
        self.player_id = player_id
        self.chess_club_id = chess_club_id
        self.score = score

    def save(self):
        with open('data/tournaments/player.json', 'r+') as file:
            try:
                players = json.load(file)
            except json.decoder.JSONDecodeError:
                players = []
            players.append(self.__dict__)
            file.seek(0)
            file.truncate()
            file.write(json.dumps(players))
            file.flush()
            file.close()

    @staticmethod
    def load_into_obj():
        with open('data/tournaments/player.json', 'r+') as file:
            try:
                players = json.load(file, object_hook=lambda d: Player(**d))
            except json.decoder.JSONDecodeError:
                players = []
        return players

    @staticmethod
    def load_into_dict():
        with open('data/tournaments/player.json', 'r+') as file:
            try:
                players = json.load(file)
                print(type(players[0]))
            except json.decoder.JSONDecodeError:
                players = []
        return players

    def update(self):
        with open('data/tournaments/player.json', 'r+') as file:
            players = self.load_into_obj()
            updated_players = []
            if players:
                for player in players:
                    if player.player_id == self.player_id:
                        updated_players.append(self.__dict__)
                    else:
                        updated_players.append(player.__dict__)
                file.seek(0)
                file.truncate()
                file.write(json.dumps(updated_players))
                file.flush()
                file.close()

    def set_player_id(self):
        players = self.load()
        if players:
            self.player_id = int(players[-1]['player_id']) + 1
        else:
            self.player_id = 0


class Match():
    match_id = itertools.count()

    def __init__(self, pair_of_players=(), match_id=-1):
        self.match_id = next(Match.match_id) if match_id == -1 else match_id
        self.pair_of_players = pair_of_players


class Round():
    def __init__(self,
                 name,
                 place,
                 round_id=-1,
                 start_datetime=datetime.now(),
                 end_datetime=None,
                 is_over=False,
                 round_matches: List[Match] = list()
                 ):
        self.name = name
        self.place = place
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.is_over = is_over
        self.round_matches = round_matches
        self.round_id = self.set_round_id() if round_id == -1 else round_id

    def set_pairs(self, tournament):
        tournament.ordonate_list_of_players()
        player = iter(tournament.list_of_players)
        matches_left = []
        for pair in zip(player, player):
            match = (
                        [pair[0].player_id, 0],
                        [pair[1].player_id, 0],
                    )
            if match not in (p.pair_of_players for p in tournament.list_of_matches):
                new_match = Match()
                new_match.pair_of_players += match
                tournament.list_of_matches.append(new_match)
                self.round_matches.append(new_match)
            else:
                for player in pair:
                    matches_left.append(player)

        if (len(tournament.list_of_players) % 2) != 0:
            tournament.uneven_number_of_players()

        if matches_left:
            self.matches_left(tournament, matches_left)

    def matches_left(self, tournament, matches_left):
        while len(matches_left) >= 2:
            while [matches_left[0], matches_left[1]] in tournament.list_of_matches:
                poped = matches_left.pop()
                matches_left.insert(0, poped)
            new_match = Match()
            new_match.pair_of_players += (
                    [matches_left[0].player_id, 0],
                    [matches_left[1].player_id, 0],
                )
            tournament.list_of_matches.append(new_match)
            self.round_matches.append(new_match)
            matches_left.pop(0)
            matches_left.pop(0)

    def save(self):
        with open('data/tournaments/round.json', 'r+') as file:
            try:
                rounds = json.load(file)
            except json.decoder.JSONDecodeError:
                rounds = []
            rounds.append(self)
            file.seek(0)
            file.truncate()
            file.write(json.dumps(rounds, default=lambda o: getattr(o, '__dict__', str(o))))
            file.flush()
            file.close()

    @staticmethod
    def load():
        with open('data/tournaments/round.json', 'r+') as file:
            try:
                rounds = [Round(**x) for x in json.load(file)]
            except json.decoder.JSONDecodeError:
                rounds = []

            if rounds:
                for round in rounds:
                    temp_matches = []
                    for match in round.round_matches:
                        temp_matches.append(Match(**match))
                    round.round_matches = temp_matches
        return rounds

    def update(self):
        with open('data/tournaments/round.json', 'r+') as file:
            rounds = self.load()
            updated_rounds = []
            if rounds:
                for round in rounds:
                    if round.round_id == self.round_id:
                        updated_rounds.append(self)
                    else:
                        updated_rounds.append(round)
                file.seek(0)
                file.truncate()
                file.write(json.dumps(updated_rounds, default=lambda o: getattr(o, '__dict__', str(o))))
                file.flush()
                file.close()

    def set_round_id(self):
        rounds = self.load()
        if rounds:
            round_id = int(rounds[-1].round_id) + 1
        else:
            round_id = 0
        return round_id

    def delete(self):
        with open('data/tournaments/round.json', 'r+') as file:
            rounds = self.load(file)
            for index, round in enumerate(rounds):
                if round.round_id == self.round_id:
                    rounds.pop(index)
                    break
            file.seek(0)
            file.truncate()
            file.write(json.dumps(rounds, default=lambda o: getattr(o, '__dict__', str(o))))
            file.flush()
            file.close()


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
        if self.current_round.round_id == 0:
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
                    tournament.current_round = Round(**tournament.current_round)
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
                file.seek(0)
                file.truncate()
                file.write(json.dumps(updated_tournaments, default=lambda o: getattr(o, '__dict__', str(o))))
                file.flush()
                file.close()
