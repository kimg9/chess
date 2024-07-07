from datetime import datetime
import itertools
import random
import json
# import uuid


class Player():
    player_id = itertools.count()
    score = 0

    def __init__(self, surname, name, birthday, chess_club_id):
        self.surname = surname 
        self.name = name
        self.birthday = birthday
        self.player_id = next(Player.player_id)
        self.chess_club_id = chess_club_id
        # self.player_id = uuid.uuid4()
    
    def set_outcome(self, status):
        if status == "win":
            self.score += 1
        elif status == "draw":
            self.score += 0.5

    def save(self):
        with open('player.json', 'a') as f:
            json.dump(self, f)
 
            
class Tournament():
    def __init__(self,name,place,start,end,current_round,list_of_players:list,list_of_rounds:list,description:str, number_of_rounds = 4):
        self.name = name
        self.place = place
        self.start = start
        self.end = end
        self.number_of_rounds = number_of_rounds
        self.current_round = current_round
        self.list_of_rounds = list_of_rounds
        self.list_of_players = list_of_players
        self.description = description
        
    def ordonate_list_of_players(self):
        if self.current_round.round_id == 0:
            random.shuffle(self.list_of_players)
        else:
            self.list_of_players =  sorted(self.list_of_players, key=lambda player: player.score, reverse=True)
            
    def uneven_number_of_players(self):
        self.current_round.pairs_list.append((self.list_of_players[-1],))
        new_match = Match()
        new_match.pair_of_player += (
                [self.list_of_players[-1].player_id, self.list_of_players[-1].score],
            )
        self.current_round.list_of_matches.append(new_match)

    def set_current_round(self):
        if self.current_round.is_over:
            for index, round in enumerate(self.list_of_rounds):
                if self.current_round == round:
                    self.current_round = self.list_of_rounds[index+1]
                    break

    def save(self):
        with open('tournament.json', 'a') as f:
            json.dump(self, f)


class Round():
    round_id = itertools.count()
    end_datetime = datetime
    is_over = False
    pairs_list = []
    list_of_matches = []

    def __init__(self, name, place, start_datetime):
        self.name = name
        self.place = place
        self.start_datetime = start_datetime
        self.round_id = next(Round.round_id)

    def set_pairs(self, tournament:Tournament):
        tournament.ordonate_list_of_players()
        player = iter(tournament.list_of_players)
        # matches_left = []
        for pair in zip(player,player):
            if pair not in self.pairs_list:
                self.pairs_list.append(pair)
                new_match = Match()
                new_match.pair_of_player += (
                        [pair[0].player_id, pair[0].score],
                        [pair[1].player_id, pair[1].score],
                    )
                self.list_of_matches.append(new_match)
            # else:
            #     for player in pair:
            #         matches_left.append(player)
                
        if (len(tournament.list_of_players)%2) != 0:
            tournament.uneven_number_of_players()
        
    #     if matches_left:
    #         self.matches_left(matches_left)
    
    # def matches_left(self, matches_left):
    #     while len(matches_left) >= 2:
    #         while [matches_left[0], matches_left[1]] in self.pairs_list:
    #             poped = matches_left.pop()
    #             matches_left.insert(0, poped)
    #         new_match = Match()
    #         new_match.pair_of_player += (
    #                 [matches_left[0].player_id, matches_left[0].score],
    #                 [matches_left[1].player_id, matches_left[1].score],
    #             )
    #         self.list_of_matches.append(new_match)
    #         matches_left.pop(0)
    #         matches_left.pop(0)
        
    def end_round(self, results):
        self.end_datetime = datetime.now()
        self.is_over = True
        
        for match in self.list_of_matches:
            if len(match.pair_of_player) != 1:
                match_set = {match.pair_of_player[0][0], match.pair_of_player[1][0]}
                for result in results:
                    if result[0][0].player_id in match_set and result[1][0].player_id in match_set:
                        result[0][0].set_outcome(result[0][1])
                        result[1][0].set_outcome(result[1][1])
            else:
                pass

    def save(self):
        with open('round.json', 'a') as f:
            json.dump(self, f)


class Match():
    match_id = itertools.count()
    pair_of_player = ()

    def __init__(self):
        self.match_id = next(Match.match_id)

    def save(self):
        with open('match.json', 'a') as f:
            json.dump(self, f)
