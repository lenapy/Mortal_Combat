from memento import Caretaker, Originator
import random


class Round:
    def __init__(self, characters=None):
        self._characters = characters or []
        for character in self._characters:
            character.set_round(self)

    def reestablish_hp_mp(self, state):
        originator = Originator()
        originator.set_state(state)
        caretaker = Caretaker()
        caretaker.set_state(originator.saved_state)
        return originator.restore_state(caretaker.get_state())

    def attack(self, attacker, attack):
        print('Attacker:', attacker.name)
        for character in self._characters:
            if character != attacker and character.is_alive():
                self.random_decision(character, attacker, attack)

    def clear_potions(self, attacker, character, attack):
        if attacker.is_under_potion() and attacker.get_number_of_attack_used_potion() + 2 == attack:
            print("potion {} is no longer active".format(attacker.is_under_potion()))
            attacker.cancel_potion()
        if character.is_under_potion() and character.get_number_of_attack_used_potion() + 2 == attack:
            print("potion {} is no longer active".format(character.is_under_potion()))
            character.cancel_potion()

    def random_decision(self, character, attacker, attack):
        self.clear_potions(character, attacker, attack)
        damage = random.randint(5, 35)
        if attacker.is_under_potion() == "Weakness":
            damage = 5
        number = random.randint(1, 11)
        if number < 7:
            self.simple_attack(character, damage)
        elif number == 7:
            self.brave_attack(attacker)
        elif number == 8:
            self.resist_with_shield(character, damage)
        elif number == 9:
            self.counter_attack(attacker, damage, character)
        elif number == 10:
            self.evade(character, damage)
        elif number == 11:
            self.cast_potion(attacker, character, damage, attack)
        print('{}, hp:{} {}, hp:{}'.format(
            character.name, character.hp, attacker.name, attacker.hp))

    def simple_attack(self, character, damage):
        character.loose_hp(damage)

    def brave_attack(self, attacker):
        attacker.hp = 100
        print("brave attack, {} successfully recharged 100% hp".format(attacker.name))

    def resist_with_shield(self, character, damage):
        character.loose_hp(int(damage / 2))
        print(character.name, "used shield. 50% damage taken")

    def evade(self, character, damage):
        if character.is_under_potion() == "Non-evade":
            character.loose_hp(damage)
            print("under Non-evade potion evade failed")
        else:
            self.reestablish_hp_mp(character)
            print(character.name, "evaded from attack")

    def cast_potion(self, attacker, character, damage, number_attack):
        if attacker.side == "Dark":
            potion = "Non-evade"
            print("{} used Non-evade potion. {} can't evade to 2 attacks".format(
                attacker.name, character.name))
        else:
            potion = "Weakness"
            print("{} used Weakness potion. {} attack has been reduced to 5 to 2 attacks".format(
                attacker.name, character.name))
        if character.is_under_potion():
            self.simple_attack(character, damage)
        else:
            character.use_potion(potion, number_attack)

    def counter_attack(self, attacker, damage, character):
        attacker.loose_hp(damage)
        print(character.name, "used counter-attack on {} damage".format(damage))
