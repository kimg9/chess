from simple_term_menu import TerminalMenu


class PlayerView():
    def new_player():
        print("To create a new player, please fill out the following information :")
        surname = input("Surname:")
        name = input("Name:")
        birthday = input("Birthday:")
        chess_club_id = input("Chess club ID:")
        return surname, name, birthday, chess_club_id
        # player = Player(surname, name, birthday, chess_club_id)
        # player.save()
        # print("You have successfully created a new player.")

    def playerslist(list_of_player):
    # Must be alphabetical order
        with open('player.json', 'r') as f:
            pass
            

class NewTournament():
    pass

class NewRound():
    # Should be called when creating new tournament
    pass
class TournamentList():
    pass

class SpecificTournament():
    pass

class TournamentPlayerList():
    pass

class TournamentRoundsMatchList():
    pass

class MainMenus():

    def first_options(self):
        print("Please chose one of the following options")
        options = ["Listes", "Rapports", "Application"]
        terminal_menu = TerminalMenu(options)   
        menu_entry_index = terminal_menu.show()
        print(f"You have selected {options[menu_entry_index]}!") 
        return options[menu_entry_index]


    def list_options():
        pass

    def report_options():
        pass

    def application():
        pass