from abc import ABCMeta, abstractmethod


class ACharacter(metaclass=ABCMeta):
    def __init__(self, name):
        self.side = None
        self.name = name
        self.hp = 100  # health points
        self.mp = 100  # mana points

    @abstractmethod
    def send_command(self, side, command):
        pass


class DarkSideCharacter(ACharacter):
    def __init__(self, name):
        super().__init__(name)
        self.side = "Dark"

    def __str__(self):
        return "{}: hp:{}, mp:{}".format(self.name, self.hp, self.mp)

    def send_command(self, side, command):
        print('{} side: {}'.format(side, self.name), command)


class LightSideCharacter(ACharacter):
    def __init__(self, name):
        super().__init__(name)
        self.side = "Light"

    def __str__(self):
        return "{}: hp:{}, mp:{}".format(self.name, self.hp, self.mp)

    def send_command(self, side, command):
        print('{} side: {}'.format(side, self.name), command)


class AFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_character(self, name):
        pass

    @staticmethod
    def get_factory(side):
        if side == 'Dark':
            return SpecificFactoryDarkSide()
        else:
            return SpecificFactoryLightSide()


class SpecificFactoryDarkSide(AFactory):
    def create_character(self, name):
        return DarkSideCharacter(name)  # initialization of a specific character


class SpecificFactoryLightSide(AFactory):
    def create_character(self, name):
        return LightSideCharacter(name)

