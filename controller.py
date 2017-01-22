from abc import abstractmethod

from factory_of_characters import ACharacter, SpecificFactoryDarkSide, SpecificFactoryLightSide


class AControlCharacters(ACharacter):
    def __init__(self):
        super().__init__(self)
        self.dark_list = list()
        self.light_list = list()

    @abstractmethod
    def add_character(self, side, name):
        pass


class ControlCharacters(AControlCharacters):
    def add_character(self, side, name):
        if side == "Dark":
            self.dark_list.append(SpecificFactoryDarkSide().create_character(name))
        else:
            self.light_list.append(SpecificFactoryLightSide().create_character(name))

    def send_command(self, side, command):
        if side == "Dark":
            characters_list = self.dark_list
        else:
            characters_list = self.light_list
        for character in characters_list:
            character.send_command(side, command)

controller = ControlCharacters()
controller.add_character("Dark", "Commander Bacara")
controller.add_character("Dark", "Ayy Vida")
controller.add_character("Dark", "Darth Vader")

controller.add_character("Light", "Agrippa Aldrete")
controller.add_character("Light", "Chewbacca")
controller.add_character("Light", "Padmé Amidala")

controller.send_command("Dark", "is ready to fight")
controller.send_command("Light", "is ready to fight")
