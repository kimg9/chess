import os, sys
source_path = os.getcwd()
sys.path.insert(0, source_path)

from packages.models import *
from datetime import datetime

player_one = Player("Dupont", "Jacques", datetime(1944,10,27),"AB12345")
player_two = Player("Aubry", "Jacqueline", datetime(1966,1,7),"AB12345")
player_three = Player("Martin", "Fanny", datetime(1980,11,16),"AB12345")
player_four = Player("Laurent", "Paul", datetime(1955,6,23),"AB12345")
player_five = Player("A", "Helena", datetime(1955,6,23),"AB12345")
player_six = Player("B", "Pierre", datetime(1955,6,23),"AB12345")
player_seven = Player("Cc", "Luc", datetime(1955,6,23),"AB12345")
player_eight = Player("D", "Jeannette", datetime(1955,6,23),"AB12345")
player_nine = Player("E", "Kim", datetime(1955,6,23),"AB12345")

def test_player_id_should_be_different():
    assert player_one.player_id not in [
        player_two.player_id, 
        player_three.player_id, 
        player_four.player_id, 
        player_five.player_id
    ]

round_one = Round(name="Round 1", place="Paris", start_datetime=datetime.now())
round_two = Round(name="Round 2", place="Paris", start_datetime=datetime.now())
round_three = Round(name="Round 3", place="Paris", start_datetime=datetime.now())
round_four = Round(name="Round 4", place="Paris", start_datetime=datetime.now())

first_tournament = Tournament(
    name="Tournament 1", 
    place="Paris", 
    start=datetime.now(), 
    end=None, 
    current_round=round_one,
    list_of_rounds=[round_one,round_two,round_three,round_four],
    list_of_players=[player_one, player_two, player_three, player_four, player_five, player_six, player_seven, player_eight, player_nine], 
    description="tournoi de Paris"
)

player_four.score = 0.5
player_three.score = 5
player_two.score = 10

def test_should_generate_matches():
    first_tournament.current_round = round_two
    round_two.set_pairs(first_tournament)
    assert round_two.list_of_matches != []
    assert len(round_two.list_of_matches[-1].pair_of_player) == 1
    assert len(round_two.pairs_list) == 5
    

my_match = [
    [
        (player_three, "win"),
        (player_two, "lose")
    ],
    [
        (player_five,"draw"),
        (player_six,"draw")
    ],
    [
        (player_five,"win"),
        (player_two,"lose")
    ]
]

def test_should_end_round_and_set_scores():
    round_one.set_pairs(first_tournament)
    round_one.end_round(my_match)
    assert round_one.is_over
    assert player_three.score == 6
    assert player_five.score == 0.5
    assert player_two.score == 10

def test_should_change_current_round():
    first_tournament.set_current_round()
    assert first_tournament.current_round == round_two
