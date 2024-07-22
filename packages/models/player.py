import json


class Player():
    """
    A class to represent a player.
    """
    def __init__(self, surname, name, birthday, chess_club_id, player_id, score=0):
        """
        Constructs all the necessary attributes for the player object.

        Attributes
        -----------
        :attr name: first name of the player
        :type name: str
        :attr surname:family name of the player
        :type surname: str
        :attr birthday: birthday of the player
        :type birthday: str (format DD/MM/YYY)
        :attr chess_club_id: birthday of the player
        :type chess_club_id: str (format AB12345)
        :attr score: score of the player
        :type score: int
        :attr player_id: ID of the player
        :type player_id: int

        """
        self.surname = surname
        self.name = name
        self.birthday = birthday
        self.player_id = player_id
        self.chess_club_id = chess_club_id
        self.score = score

    def save(self):
        """
        Saves the Player object to the database.
        Loads all the DB, append the object to the list, clear the file and write everything back.
        """
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
        """
        Loads all the Player and convert them to Player Python object.
        """
        with open('data/tournaments/player.json', 'r+') as file:
            try:
                players = json.load(file, object_hook=lambda d: Player(**d))
            except json.decoder.JSONDecodeError:
                players = []
        return players

    @staticmethod
    def load_into_dict():
        """
        Loads all the Players and converts them to a list of dict.
        """
        with open('data/tournaments/player.json', 'r+') as file:
            try:
                players = json.load(file)
            except json.decoder.JSONDecodeError:
                players = []
        return players

    def update(self):
        """
        Update an entry of Player in the database.
        Loads all the Players as Python objects.
        Replace the old values of self by the new ones.
        Clears the file and writes everything back.
        """
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
        """
        Sets player ID.
        Loads all player, get ID from last player in DB and sets player ID to the next number.
        """
        players = self.load_into_dict()
        if players:
            self.player_id = int(players[-1]['player_id']) + 1
        else:
            self.player_id = 0
