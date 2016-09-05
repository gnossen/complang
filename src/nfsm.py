from fsm import NFSM
from fsm_state import FSMState

class NFSM(FSM):
    def __init__(self, letter_cls):
        super(NFSM, self).__init__(letter_cls)
        self.make_dead_state()

    def make_dead_state(self):
        self.dead_state = FSMState([])
        self.dead_state._id = 0
        self.states += [self.dead_state]

    def reverse_ids(self):
        def _reverse_ids(state):
            if not state.visited:
                state._id = self.state_count - state._id
                state.visit()
                for _, next_state in state.edges:
                    _reverse_ids(next_state)

        _reverse_ids(self.initial_state)
        self._clear_visited()

    def _connect_dead_state(self, state):
        dead_transitions = set()
        for letter in self._letter_cls.all():
            if letter.id() not in state.valid_transitions():
                dead_transitions = dead_transitions | {letter.id()}

        state.add_edges([(dead_transitions, self.dead_state)])

    def connect_dead_state(self):
        for state in self.states:
            if state is not self.dead_state:
                self._connect_dead_state(state)

    def is_impossible(self, state):
        if state is self.dead_state:
            return False

        if state.terminal:
            return False

        for letters, subs_state in state.edges:
            if subs_state is not self.dead_state and \
                    not (len(letters) == 1 and tuple(letters)[0] == -1):
                return False

        return True

    def remove_impossible(self, state):
        # pdb.set_trace()
        epsilon_edges = state.get_epsilon_edges()
        for other_state in self.states:
            if state is other_state:
                continue

            edges_to = other_state.get_edges_to(state)
            if len(edges_to) != 0:
                other_state.remove_edges_to(state)
                new_edges = []
                for incoming_letters, _ in edges_to:
                    for _, destination_state in epsilon_edges:
                        new_edges += [(incoming_letters, destination_state)]

                other_state.add_edges(new_edges)

    def remove_impossible_states(self):
        for state in self.states:
            if self.is_impossible(state):
                self.remove_impossible(state)

    def from_regex(self, ast):
        self.initial_transitions = self._from_regex(ast)
        self.initial_state = FSMState([self.initial_transitions])
        self._add_state(self.initial_state)
        self.connect_dead_state()
        self.reverse_ids()
        self._clear_visited()
        self.remove_impossible_states()
        
    def _from_regex(self, ast, next_transition=None):
        if ast.type == RegexASTNode.CAT_EXPR:
            transition_B = self._from_regex(ast.right, next_transition=next_transition)
            mid_state = FSMState([transition_B])
            self._add_state(mid_state)
            transition_A = self._from_regex(ast.left, next_transition=(-1, mid_state))
            return transition_A
        elif ast.type == RegexASTNode.LETTER:
            state_B = None
            if next_transition is None:
                state_B = FSMState([], terminal=True)
                self._add_state(state_B)
            else:
                _, state_B = next_transition

            return (ast.value.id(), state_B)
        elif ast.type == RegexASTNode.EPSILON:
            state_B = None
            if next_transition is None:
                state_B = FSMState([], terminal=True)
                self._add_state(state_B)
            else:
                _, state_B = next_transition

            return (-1, state_B)
        elif ast.type == RegexASTNode.OR_EXPR:
            if next_transition is None:
                final_state = FSMState([], terminal=True)
                self._add_state(final_state)
                next_transition = (-1, final_state)

            transitions_A = self._from_regex(ast.left, next_transition=next_transition)
            transitions_B = self._from_regex(ast.right, next_transition=next_transition)
            or_initial_state = FSMState([transitions_A, transitions_B])
            self._add_state(or_initial_state)
            return (-1, or_initial_state)
        elif ast.type == RegexASTNode.REP_EXPR:
            terminal = (next_transition is None)
            loop_state = FSMState([], terminal=terminal)
            loop_init_transition = self._from_regex(ast.left, next_transition=(-1, loop_state))

            if next_transition is not None:
                loop_state.add_edges([loop_init_transition, next_transition])
            else:
                loop_state.add_edges([loop_init_transition])

            self._add_state(loop_state)
            return (-1, loop_state)
        else:
            raise Exception("Unknown AST type.")
