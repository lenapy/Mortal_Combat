from abc import ABCMeta, abstractmethod


class ACharacter(metaclass=ABCMeta):
    def __init__(self, name):
        self.side = None
        self.name = name
        self.hp = 100  # health points
        self.mp = 100  # mana points

    def __str__(self):
        return "{}: hp:{}, mp:{}".format(self.name, self.hp, self.mp)


class DarkSideCharacter(ACharacter):
    def __init__(self, name):
        super().__init__(name)
        self.side = "Dark"


class LightSideCharacter(ACharacter):
    def __init__(self, name):
        super().__init__(name)
        self.side = "Light"


class AFactory(metaclass=ABCMeta):
    @abstractmethod
    def create_character(self, name):
        pass


class SpecificFactoryDarkSide(AFactory):
    def create_character(self, name):
        return DarkSideCharacter(name)  # initialization of a specific character


class SpecificFactoryLightSide(AFactory):
    def create_character(self, name):
        return LightSideCharacter(name)


character = "Side"
if character == "DarkSide":
    specific_factory = SpecificFactoryDarkSide()
else:
    specific_factory = SpecificFactoryLightSide()

print(specific_factory.create_character("vasya"))


class ControlCharacter:
    def __init__(self):
        self.dark_list = list()
        self.light_list = list()

    def add_character(self, side, name):
        if side == "Dark":
            self.dark_list.append(SpecificFactoryDarkSide().create_character(name))
        else:
            self.light_list.append(SpecificFactoryLightSide().create_character(name))

control = ControlCharacter()
control.add_character("Dark", "character1")
