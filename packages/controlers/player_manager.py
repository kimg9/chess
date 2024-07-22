import packages.views.player_view as player_view
import packages.controlers.menu_manager as menu_manager_controler
import packages.models.player as player_model


class PlayerManager():
    @classmethod
    def player_options_menu(self):
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
        sorted_list_of_players = sorted(players, key=lambda d: d['surname'])
        header = sorted_list_of_players[0].keys()
        rows = [v.values() for v in sorted_list_of_players]
        player_view.PlayerView.list_players_alphabetically(rows, header)
