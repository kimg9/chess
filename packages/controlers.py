import json

"""
Steps : 

- Initiate a new tournament (user input)
- Initiate new players (user input)
- Initiate rounds ? (view)

(- generate_matches(tournament) on first round of tournament
- ask for results (user input)
- end_round with matches result list
- set_current_round on Tournament to change rounds)
*tournament.number_of_rounds

"""

data = 0

with open('data.json', 'w') as f:
    json.dump(data, f)