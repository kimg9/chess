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
        """
        Set player ID
        """
        players = self.load_into_dict()
        if players:
            self.player_id = int(players[-1]['player_id']) + 1
        else:
            self.player_id = 0
