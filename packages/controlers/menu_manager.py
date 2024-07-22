import packages.views.main_menu as main_menu_view
import packages.controlers.player_manager as player_manager_controler
import packages.controlers.tournament_manager as tournament_manager_controler


class MenuManager():
    @staticmethod
    def select_object_menu():
        answer = main_menu_view.MainMenus.select_object()
        match answer['select_object']:
            case 'Player':
                player_manager_controler.PlayerManager.player_options_menu()
            case 'Tournament':
                tournament_manager_controler.TournamentManager.tournament_options_menu()
            case 'Exit':
                exit()


class Application():
    def main():
        MenuManager.select_object_menu()
