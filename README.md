# Chess Tournament Manager

## Introduction

This application is a standalone, offline program designed to manage chess tournaments. It is written in Python and can be executed from the console using the command:

```bash
python chess.py
```
Dependencies required for the program are listed in the `requirements.txt` file.

## Code Structure
The program follows the Model-View-Controller (MVC) design pattern and is divided into three main packages:
- **models**: Contains data structures and logic.
- **views**: Handles the user interface.
- **controllers**: Manages the interaction between models and views.

## Data Structure
### Player Management
- Last Name
- First Name
- Date of Birth
- National Chess ID (unique, format: two letters followed by five digits, e.g., AB12345).
- Player ID

### Tournament Management
- Name
- Location
- Start Date
- End Date
- Number of Rounds (default is 4)
- Current Round Number
- List of Rounds
- List of matches
- List of Registered Players
- Description (for deneral remarks by the Tournament Director)

### Rounds
- Name (e.g., "Round 1")
- Place
- Start Date and Time (automatically filled when the round starts).
- End Date and Time (automatically filled when the round ends).
- Is_over status (yes or no)
- List of matches for this round
- Round ID

### Matches
- Match ID
- A pair of players

## Features
### Points Allocation
- Winner: 1 point
- Loser: 0 points
- Draw: 0.5 points each

### Reports
- Tthe following reports are available:
  - List of all players in alphabetical order.
  - List of all tournaments.
  - Name and dates of a given tournament.
  - List of players in a tournament in alphabetical order.
  - List of all rounds and matches in a tournament.

## Installation and Setup
1. Clone the repository.
2. Navigate to the project directory.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run the program:

```bash
python chess.py
```

5. Generate a new `flake8` report:

```bash
flake8 --max-line-length=119 --format=html --htmldir=flake8_rapport
```