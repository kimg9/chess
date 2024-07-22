from datetime import datetime
from typing import List
import itertools
import json


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
                 is_over="No",
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
