from datetime import datetime
import itertools
import json


class Match():
    """
    A class to represent a match.
    """
    match_id = itertools.count()

    def __init__(self, pair_of_players=(), match_id=-1):
        """
        Constructs all the necessary attributes for the match object.

        Attributes
        -----------
        :attr name: a pair of two players objects
        :type name: list
        :attr match_id: ID of the match
        :type match_id: int

        """
        self.match_id = next(Match.match_id) if match_id == -1 else match_id
        self.pair_of_players = pair_of_players


class Round():
    """
    A class to represent a round.
    """
    def __init__(self,
                 name,
                 place,
                 round_matches=None,
                 round_id=-1,
                 start_datetime=datetime.now(),
                 end_datetime=None,
                 is_over="No",
                 ):
        """
        Constructs all the necessary attributes for the round object.

        Attributes
        -----------
        :attr name: name of the round
        :type name: str
        :attr place: place of the round
        :type place: str
        :attr start_datetime: start datetime of the round
        :type start_datetime: datetime (default = now())
        :attr end_datetime: end datetime of the round
        :type end_datetime: datetime (default = None)
        :attr is_over: is_over status of the round
        :type is_over: str (defautl = "No")
        :attr round_matches: list of all matches for this round
        :type round_matches: List[Match] (default = list())
        :attr round_id: ID of the round
        :type round_id: int

        """
        self.name = name
        self.place = place
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.is_over = is_over
        self.round_matches = round_matches if round_matches is not None else []
        self.round_id = self.set_round_id() if round_id == -1 else round_id

    def set_pairs(self, tournament):
        """
        Sets pairs of players and creates a Match object.

        :attr tournament: tournament of the round
        :type tournament: Tournament
        """
        tournament.ordonate_list_of_players()
        player = iter(tournament.list_of_players)
        players_left = []

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
            elif match in (p.pair_of_players for p in tournament.list_of_matches):
                for player in pair:
                    players_left.append(player)

        if (len(tournament.list_of_players) % 2) != 0:
            solo_match = tournament.uneven_number_of_players()
            self.round_matches.append(solo_match)
            tournament.list_of_matches.append(solo_match)

        if players_left:
            self.players_left(tournament, players_left)

    def players_left(self, tournament, players_left):
        """
        Sets pairs of players for players that have already met during a match.

        :attr tournament: tournament of the round
        :type tournament: Tournament
        :attr players_left: list of all the players left
        :type players_left: List[Player]
        """
        while len(players_left) >= 2:
            while [players_left[0], players_left[1]] in (p.pair_of_players for p in tournament.list_of_matches):
                poped = players_left.pop()
                players_left.insert(0, poped)
            new_match = Match()
            new_match.pair_of_players += (
                    [players_left[0].player_id, 0],
                    [players_left[1].player_id, 0],
                )
            tournament.list_of_matches.append(new_match)
            self.round_matches.append(new_match)
            players_left.pop(0)
            players_left.pop(0)

    def save(self):
        """
        Saves the Round object to the database.
        Loads all the DB, appends the object to the list, clears the file and writes everything back.
        """
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
        """
        Loads all the Rounds and converts them to Round Python object.
        Converts all the matches in the round_matches attributes to instance of Match objects.
        """
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
        """
        Updates an entry of Round in the database.
        Loads all the Rounds as Python objects.
        Replaces the old values of self by the new ones.
        Clears the file and writes everything back.
        """
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
        """
        Sets round ID.
        Loads all round, gets ID from last round in DB and sets round ID to the next number.
        """
        rounds = self.load()
        if rounds:
            round_id = int(rounds[-1].round_id) + 1
        else:
            round_id = 0
        return round_id
