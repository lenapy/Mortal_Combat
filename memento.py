class Originator:
    def __init__(self):
        self._state = None

    def set_state(self, value):
        self._state = value

    @property
    def saved_state(self):
        return Memento(self._state)

    def restore_state(self, memento):
        state = memento.get_state()
        print(state)
        self.set_state(state)


class Memento:
    def __init__(self, state):
        self._state = state

    def get_state(self):
        return self._state


class Caretaker:
    def __init__(self):
        self._state = None

    def set_state(self, state):
        self._state = state

    def get_state(self):
        return self._state