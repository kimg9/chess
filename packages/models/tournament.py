from packages.models.round import Round, Match
from packages.models.player import Player
import random
import json


class Tournament():
    """
    A class to represent a tournament.
    """
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
        """
        Constructs all the necessary attributes for the tournament object.

        Attributes
        -----------
        :attr name: name of the tournament
        :type name: str
        :attr place: place of the tournament
        :type place: str
        :attr start: start date of the tournament
        :type start: str (formation DD/MM/YYY)
        :attr end: end date of the tournament
        :type end: str (formation DD/MM/YYY)
        :attr number_of_rounds: number of rounds of the tournament
        :type number_of_rounds: int
        :attr current_rounds: current round in tournament
        :type current_rounds: Round
        :attr list_of_rounds: list of rounds of the tournament
        :type list_of_rounds: List[Round]
        :attr list_of_matches: list of matches of the tournament
        :type list_of_matches: List[Match]
        :attr list_of_players: list of players of the tournament
        :type list_of_players: List[Player]
        :attr description: description of the tournament
        :type description: str

        """
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
        """
        Ordonnates player according to score or randowly if it's the first round.
        """
        if len(self.list_of_rounds) == 1:
            random.shuffle(self.list_of_players)
        else:
            self.list_of_players = sorted(self.list_of_players, key=lambda player: player.score, reverse=True)

    def uneven_number_of_players(self):
        """
        In case of an uneven number of players, append the last player to a match solo.
        """
        new_match = Match()
        new_match.pair_of_players += (
                [self.list_of_players[-1].player_id, 0],
            )
        self.list_of_matches.append(new_match)

    def save(self):
        """
        Saves the Tournament object to the database.
        Loads all the DB, append the object to the list, clear the file and write everything back.
        """
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
        """
        Loads all the Tournaments and converts them to a list of dict.
        """
        with open('data/tournaments/tournament.json', 'r+') as file:
            try:
                tournaments = json.load(file)
            except json.decoder.JSONDecodeError:
                tournaments = []
        return tournaments

    @staticmethod
    def load_into_obj():
        """
        Loads all the Tournament and converts them to Tournament Python object.
        Converts all instances in list_of_players as Player objects.
        Converts all instances in list_of_matches as Match objects.
        Converts all instances in list_of_rounds as Round objects.
        Converts instance in current_round as Round objects.
        """
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
        """
        Updates an entry of Tournament in the database.
        Loads all the Tournaments as Python objects.
        Replaces the old values of self by the new ones.
        Clears the file and writes everything back.
        """
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
