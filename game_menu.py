from abc import ABCMeta, abstractmethod
import pickle


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
        self._context.set_state(Context.STATE_SHOW_CHARACTERS_INFO)
        self._context.set_state(Context.STATE_SELECT_PLAYER)


class StateShowCharactersInfo(AState):
    def handle(self):
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



