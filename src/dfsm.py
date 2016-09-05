from fsm import FSM
from nfsm import NFSM

class DFSM(FSM):
    def from_regex(self, ast):
        nfsm = NFSM(self._letter_cls)
        nfsm.from_regex(ast)
        self.from_nfsm(nfsm)

    def from_nfsm(self, nfsm):
        self.dead_state = FSMSuperState({nfsm.dead_state}, [])
        self._add_state(self.dead_state)
        self.initial_state = FSMSuperState({nfsm.initial_state}, [])
        self._add_state(self.initial_state)
        with self.traverse():
            self._from_nfsm(nfsm, self.initial_state)

    def get_by_ref_states(self, ref_states):
        for state in self.states:
            if ref_states == state.component_states:
                return state
        else:
            return None

    def make_state(self, component_states):
        ref_state = self.get_by_ref_states(component_states)
        if ref_state is None:
            ref_state = FSMSuperState(component_states, [])
            self._add_state(ref_state)

        return ref_state

    def _from_nfsm(self, nfsm, state):
        if not state.visited:
            state.visit()
            paths = []

            for letter in self._letter_cls.all():
                this_letter_states = state.nd_transition(letter.id(), nfsm)
                next_state = self.make_state(this_letter_states)

                paths += [(letter.id(), next_state)]

            state.add_edges(paths)
            for _, next_state in state.edges:
                self._from_nfsm(nfsm, next_state)

