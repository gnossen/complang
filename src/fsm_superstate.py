from fsm_state import FSMState

class FSMSuperState(FSMState):
    # component_states expected to be a set
    def __init__(self, component_states, edges, id=None, terminal=False):
        super(FSMSuperState, self).__init__(edges, id=id, terminal=terminal)
        self.component_states = component_states
        self.set_terminal()

    def set_terminal(self):
        for component_state in self.component_states:
            self.terminal |= component_state.terminal

    def __eq__(self, other):
        if type(other) is FSMState:
            if len(self.component_states) == 1:
                return self.component_states[0] == other

        if type(other) is not FSMSuperState:
            return False

        same = True
        for component_state in self.component_states:
            same = same and (component_state in other.component_states)

    def nd_transition(self, letter_id, nfsm):
        new_states = set()
        for component_state in self.component_states:
            with nfsm.traverse():
                new_states = new_states | component_state.nd_transition(letter_id)

        return new_states
