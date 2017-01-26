from memento import Memento, Caretaker, Originator


class Fight:
    def __init__(self, user_player, comp_enemy):
        self.user_player = user_player
        self.comp_enemy = comp_enemy

    def reestablish_hp_mp(self, state):
        originator = Originator()
        originator.set_state(state)
        caretaker = Caretaker()
        caretaker.set_state(originator.saved_state)
        return originator.restore_state(caretaker.get_state())

    def __str__(self):
        return "{}, {}".format(self.user_player, self.comp_enemy)

