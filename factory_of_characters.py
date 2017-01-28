from abc import ABCMeta, abstractmethod


class ACharacter(metaclass=ABCMeta):
    def __init__(self, name):
        self.side = None
        self.name = name
        self.hp = 100  # health points
        self.mp = 100  # mana points
        self.round_ = None
        self.potion = None
        self.attack_number = None

    @abstractmethod
    def send_command(self, side, command):
        pass

    def set_round(self, round_):
        self.round_ = round_

    def attack(self, attack):
        self.round_.attack(self, attack)

    def loose_hp(self, value):
        print(
            '%s Loose HP:' % self.name,
            value)
        self.hp -= value

    def loose_mp(self, value):
        print(
            '%s Loose MP:' % self.name,
            value)
        self.mp -= value

    def is_alive(self):
        return self.hp > 0 and self.mp > 0

    def use_potion(self, potion, attack):
        self.attack_number = attack
        self.potion = potion

    def is_under_potion(self):
        return self.potion

    def cancel_potion(self):
        self.potion = None
        self.attack_number = None

    def get_number_of_attack_used_potion(self):
        return self.attack_number


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

