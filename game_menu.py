from abc import ABCMeta, abstractmethod
import pickle
import os

from controller import controller
from factory_of_characters import AFactory
from fight import Round


class AShowCharactersInfo(metaclass=ABCMeta):
    DATA_FILE = "characters_data"

    @abstractmethod
    def read_file(self):
        pass

    @abstractmethod
    def show_info(self, name):
        pass


class ShowCharactersInfo(AShowCharactersInfo):

    def read_file(self):
        try:
            with open(self.DATA_FILE, 'rb') as f:
                return pickle.load(f)
        except IOError:
            return []

    def show_info(self, name):
        data = self.read_file()
        for characters in data:
            for char_name, char_info in characters.items():
                if char_name == name:
                    print(char_info)


class ProxyShowCharactersInfo(AShowCharactersInfo):
    def __init__(self, show_characters_info):
        self.show_characters_info = show_characters_info
        self.data = None

    def read_file(self):
            try:
                with open(self.DATA_FILE, 'rb') as f:
                    return pickle.load(f)
            except IOError:
                return []

    def show_info(self, name):
        if not self.data:
            data = self.read_file()
            self.data = data
            for characters in data:
                for char_name, char_info in characters.items():
                    if char_name == name:
                        print(char_info)
        else:
            for data_characters in self.data:
                for data_name, data_info in data_characters.items():
                    if data_name == name:
                        print(data_info)


class AState(metaclass=ABCMeta):
    def __init__(self, context):
        self._context = context

    @abstractmethod
    def handle(self):
        pass


class StateShowMenu(AState):
    side = "Light"

    def handle(self):
        user_input_1 = input("Choose side:\n`Dark`,"
                             " press 1\n`Light`, press 2")
        if user_input_1 == '1':
            StateShowMenu.side = "Dark"
            controller.send_command("Dark", "is ready to fight")
        else:
            StateShowMenu.side = "Light"
            controller.send_command("Light", "is ready to fight")
        user_input_2 = input("To choose character, press 1\n"
                             "To read info about characters, press 2")
        if user_input_2 == '1':
            os.system('clear')
            self._context.set_state(Context.STATE_SELECT_PLAYER)
        else:
            os.system('clear')
            self._context.set_state(Context.STATE_SHOW_CHARACTERS_INFO)


class StateShowCharactersInfo(AState):

    def handle(self):
        print(StateShowMenu.side)
        info = ProxyShowCharactersInfo(ShowCharactersInfo)
        if StateShowMenu.side == "Light":
            characters_list = controller.light_list
        else:
            characters_list = controller.dark_list
        for character in characters_list:
            name = character.name
            print('*'*6, name, '*'*6)
            info.show_info(name)
        user_input_3 = input("To choose character, press 1\n"
                             "To change side, press 2")
        if user_input_3 == "1":
            os.system('clear')
            self._context.set_state(Context.STATE_SELECT_PLAYER)
        else:
            os.system('clear')
            self._context.set_state(Context.STATE_SHOW_MENU)


class StateSelectPlayer(AState):
    players = []

    def handle(self):
        if StateShowMenu.side == "Light":
            lst = [0, 'Agrippa Aldrete', 'Chewbacca', 'Padmé Amidala']
        else:
            lst = [0, 'Commander Bacara', 'Ayy Vida', 'Darth Vader']
        for num, name in enumerate(lst):
            if num == 0:
                continue
            else:
                print(num, name)
        user_input_4 = input("Enter number of character: ")
        player_name = lst[int(user_input_4)]
        player_side = StateShowMenu.side
        player = {'name': player_name, 'side': player_side}
        StateSelectPlayer.players.append(player)
        if len(StateSelectPlayer.players) == 2:
            os.system('clear')
            self._context.set_state(Context.STATE_PLAY_GAME)
        else:
            os.system('clear')
            print("Now you can choose enemy for your player:")
            self._context.set_state(Context.STATE_SHOW_MENU)


class StatePlayGame(AState):

    def handle(self):
        user_player = AFactory.get_factory(StateSelectPlayer.players[0]['side']).create_character(
            StateSelectPlayer.players[0]['name'])
        comp_enemy = AFactory.get_factory(StateSelectPlayer.players[1]['side']).create_character(
            StateSelectPlayer.players[1]['name'])
        Round(characters=(user_player, comp_enemy))
        attack = 1
        while user_player.is_alive() and comp_enemy.is_alive():
            print("attack ", attack)
            print("*" * 20)
            user_player.attack(attack)
            if comp_enemy.is_alive():
                print("*" * 20)
                comp_enemy.attack(attack)
                print("*" * 20)
                print("\n")
            attack += 1
        else:
            winner = user_player if user_player.is_alive() else comp_enemy
            print("Winner:", winner.name)
            exit()


class Context:
    STATE_SHOW_MENU = 'show_menu'
    STATE_SHOW_CHARACTERS_INFO = 'show_characters_info'
    STATE_SELECT_PLAYER = 'select a player'
    STATE_PLAY_GAME = 'play game'

    def __init__(self, state=STATE_SHOW_MENU):
        self._state = None
        self.set_state(state)

    def set_state(self, state):
        if state == self.STATE_SHOW_MENU:
            self._state = StateShowMenu(self)
        elif state == self.STATE_SHOW_CHARACTERS_INFO:
            self._state = StateShowCharactersInfo(self)
        elif state == self.STATE_SELECT_PLAYER:
            self._state = StateSelectPlayer(self)
        elif state == self.STATE_PLAY_GAME:
            self._state = StatePlayGame(self)

    def next_state(self):
        self._state.handle()

if __name__ == "__main__":
    context = Context(Context.STATE_SHOW_MENU)
    while True:
        context.next_state()
