import packages.views.player_view as player_view
import packages.controlers.menu_manager as menu_manager_controler
import packages.models.player as player_model


class PlayerManager():
    """
    A class to represent the options contained in the "Player" menu
    """
    @classmethod
    def player_options_menu(self):
        """
        Redirects the user to the correct method depending on the selected option.
        There are 3 options the user can chose from.
        """
        answer = player_view.PlayerView.select_options_player()
        match answer['select_options_player']:
            case 'Create new player':
                self.create_new_player()
                player = player_view.PlayerView()
                player.successful_create_player()
                self.player_options_menu()
            case 'List all players in alphabetical order':
                self.list_players_alphabetically(player_model.Player.load_into_dict())
                self.player_options_menu()
            case 'Return':
                menu_manager_controler.MenuManager().select_object_menu()

    @classmethod
    def create_new_player(self):
        """
        Redirects to a view where the user fills a form
        then uses the information filled to create a new instance of a Player object
        initialized a new ID for the player then saves it to the DB.
        """
        answers = player_view.PlayerView.create_player()
        player = player_model.Player(
            player_id=0,
            surname=answers['player_surname'],
            name=answers['player_name'],
            birthday=answers['player_birthday'],
            chess_club_id=answers['player_chess_club_id']
        )
        player.set_player_id()
        player.save()

    def list_players_alphabetically(players):
        """
        Uses a list of Player objects loaded as dicts and sorts
        them alphabetically by surname. It then created the header with the keys
        of the dict and the rows with its value and sends it to a view to create
        the table that will be displayed.

        :param players: loaded players from DB
        :type players: list of Player dict

        """
        sorted_list_of_players = sorted(players, key=lambda d: d['surname'])
        header = sorted_list_of_players[0].keys()
        rows = [v.values() for v in sorted_list_of_players]
        player_view.PlayerView.list_players_alphabetically(rows, header)
