from abc import ABCMeta, abstractmethod
import pickle

from controller import controller


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
    def handle(self):
        user_input_1 = input("Choose your side:\n`Dark`,"
                             " press 1\n`Light`, press 2")
        if user_input_1 == '1':
            controller.send_command("Dark", "is ready to fight")
        else:
            controller.send_command("Light", "is ready to fight")
        user_input_2 = input("To choose character, press 1\n"
                             "To read info about character, press 2")
        if user_input_2 == '1':
            self._context.set_state(Context.STATE_SELECT_PLAYER)
        else:
            self._context.set_state(Context.STATE_SHOW_CHARACTERS_INFO)


class StateShowCharactersInfo(AState):
    def handle(self):
        proxy = ProxyShowCharactersInfo(ShowCharactersInfo)
        proxy.show_info('Agrippa Aldrete')

        self._context.set_state(Context.STATE_SHOW_MENU)
        self._context.set_state(Context.STATE_SELECT_PLAYER)


class StateSelectPlayer(AState):
    def handle(self):
        self._context.set_state(Context.STATE_SHOW_MENU)
        self._context.set_state(Context.STATE_SHOW_CHARACTERS_INFO)


class Context:
    STATE_SHOW_MENU = 'show_menu'
    STATE_SHOW_CHARACTERS_INFO = 'show_characters_info'
    STATE_SELECT_PLAYER = 'select a player'

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

    def next_state(self):
        self._state.handle()

context = Context(Context.STATE_SHOW_MENU)
context.next_state()
context.next_state()
