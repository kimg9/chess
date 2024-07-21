# Chess Tournament Manager

## Introduction

This application is a standalone, offline program designed to manage chess tournaments. It is written in Python and can be executed from the console using the command:

```bash
python chess.py
```
Dependencies required for the program are listed in the `requirements.txt` file.

## Features
### Points Allocation
- Winner: 1 point
- Loser: 0 points
- Draw: 0.5 points each

### Reports
- Display the following reports:
  - List of all players in alphabetical order.
  - List of all tournaments.
  - Name and dates of a given tournament.
  - List of players in a tournament in alphabetical order.
  - List of all rounds and matches in a tournament.

## Code Structure
The program follows the Model-View-Controller (MVC) design pattern and is divided into three main packages:
- **models**: Contains data structures and logic.
- **views**: Handles the user interface.
- **controllers**: Manages the interaction between models and views.

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

## Conclusion
This Chess Tournament Manager application provides a comprehensive solution for managing players, tournaments, and matches in an offline environment. With robust data persistence, dynamic pairing, and easy-to-generate reports, it meets the needs of chess club managers efficiently.