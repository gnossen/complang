from regex import *
import pydot
import copy

class FSM:
    def __init__(self, letter_class):
        self.letter_class = letter_class
        self.initial_state = None
        self.states = []
        self.state_count = 1

        self.make_dead_state()

    def make_dead_state(self):
        self.dead_state = FSMState([])
        self.dead_state._id = 0
        self.states += [self.dead_state]

    def get_state(self, id):
        for state in self.states:
            if state._id == id:
                return state
        else:
            return None

    def clear_visited(self):
        for state in self.states:
            state.clear_visited()

    def add_state(self, state):
        state._id = self.state_count
        self.state_count += 1
        self.states += [state]
        self.connect_dead_state(state)

    def connect_dead_state(self, state):
        dead_transitions = set()
        for letter in self.letter_class.all():
            if letter.id() not in state.valid_transitions():
                dead_transitions = dead_transitions | {letter.id()}

        state.add_edges([(dead_transitions, self.dead_state)])

    def draw(self, filename, show_dead=False):
        graph = pydot.Dot(graph_type='digraph')
        state_hash = {}
        def _draw(state):
            if not state.visited:
                node = pydot.Node(str(state._id), label=('"%s"' % str(state._id)))
                if state.terminal:
                    node.set_shape('"doublecircle"')
                else:
                    node.set_shape('"circle"')

                graph.add_node(node)
                state_hash[state] = node
                state.visit()

                for transition_set, new_state in state.edges:
                    if new_state is not self.dead_state or show_dead:
                        new_node = _draw(new_state) 
                        letter_str_list = []
                        for letter_id in list(transition_set):
                            if letter_id == -1:
                                letter_str_list += ["0"]
                            else:
                                letter_str_list += [str(self.letter_class(letter_id))]

                        edge_label = '"' +  ", ".join(letter_str_list) + '"'
                        graph_edge = pydot.Edge(node, new_node) 
                        graph_edge.set_label(edge_label)
                        graph.add_edge(graph_edge)

                return node
            else:
                return state_hash[state]

        _draw(self.initial_state)
        graph.write_png(filename)
        self.clear_visited()

class NFSM(FSM):
    def reverse_ids(self):
        def _reverse_ids(state):
            if not state.visited:
                state._id = self.state_count - state._id
                state.visit()
                for _, next_state in state.edges:
                    _reverse_ids(next_state)

        _reverse_ids(self.initial_state)
        self.clear_visited()

    def from_regex(self, ast):
        self.initial_transitions = self._from_regex(ast)
        self.initial_state = FSMState([self.initial_transitions])
        self.add_state(self.initial_state)
        self.reverse_ids()

    def _from_regex(self, ast, next_transition=None):
        if ast.type == RegexASTNode.CAT_EXPR:
            transition_B = self._from_regex(ast.right, next_transition=next_transition)
            mid_state = FSMState([transition_B])
            self.add_state(mid_state)
            transition_A = self._from_regex(ast.left, next_transition=(-1, mid_state))
            return transition_A
        elif ast.type == RegexASTNode.LETTER:
            state_B = None
            if next_transition is None:
                state_B = FSMState([], terminal=True)
                self.add_state(state_B)
            else:
                _, state_B = next_transition

            return (ast.value.id(), state_B)
        elif ast.type == RegexASTNode.EPSILON:
            state_B = None
            if next_transition is None:
                state_B = FSMState([], terminal=True)
                self.add_state(state_B)
            else:
                _, state_B = next_transition

            return (-1, state_B)
        elif ast.type == RegexASTNode.OR_EXPR:
            if next_transition is None:
                final_state = FSMState([], terminal=True)
                self.add_state(final_state)
                next_transition = (-1, final_state)

            transitions_A = self._from_regex(ast.left, next_transition=next_transition)
            transitions_B = self._from_regex(ast.right, next_transition=next_transition)
            or_initial_state = FSMState([transitions_A, transitions_B])
            self.add_state(or_initial_state)
            return (-1, or_initial_state)
        elif ast.type == RegexASTNode.REP_EXPR:
            terminal = (next_transition is None)
            loop_state = FSMState([], terminal=terminal)
            loop_init_transition = self._from_regex(ast.left, next_transition=(-1, loop_state))
            loop_state.add_edges([loop_init_transition, next_transition])
            self.add_state(loop_state)
            return (-1, loop_state)
        else:
            raise Exception("Unknown AST type.")

class FSMState:
    def __init__(self, edges, id=None, terminal=False):
        # edges is expected to be of the form
        #    [ ({letter1_id1, letter1_id2}, new_state1), ... , (lettern_id, new_staten)]
        self.edges = []
        self._id = id
        self.add_edges(edges)
        self.visited = False

        self.terminal = terminal

    def __hash__(self):
        return hash(self._id)

    def clear_visited(self):
        self.visited = False

    def visit(self):
        self.visited = True

    def add_edges(self, edges):
        for edge, new_state in edges:
            if type(edge) is set:
                self.edges += [(edge, new_state)]
            else:
                self.edges += [({edge}, new_state)]

    # only call on deterministic nodes
    def transition(self, letter):
        for edge_letter_set, state in self.edges:
            for edge_letter in edge_letter_set:
                if edge_letter == letter:
                    return state

        return None

    def valid_transitions(self):
        letters = set()
        for transition_letters, next_state in self.edges:
            letters = letters | set(transition_letters)

        return letters

    def nd_transition(self, letter):
        new_states = set()
        for edge_letter_set, state in self.edges:
            if letter in edge_letter_set:
                new_states = new_states | {state}

            if -1 in edge_letter_set:
                new_states = new_states | state.nd_transition(letter)

        return new_states

    def __eq__(self, other):
        return self._id == other._id

class DFSM(FSM):
    def from_nfsm(self, nfsm):
        self.state_count = nfsm.state_count
        self.initial_state = copy.deepcopy(nfsm.initial_state)
        self.populate_state_list()
        self._from_nfsm(nfsm, self.initial_state)

    def populate_state_list(self):
        def visit_state(state):
            if not state.visited:
                self.states += [state]
                state.visit()

                for letters, new_state in state.edges:
                    visit_state(new_state)

        visit_state(self.initial_state)

    def _from_nfsm(self, nfsm, state):
        if not state.visited():
            state.visit()
            nfsm_state = nfsm.get_state(state._id)
            paths = []
            for letter in state.valid_transitions():
                this_letter_transitions = state.nd_transition(letter)
                next_state = None
                if len(this_letter_transitions) > 1:
                    next_state = FSMSuperState(this_letter_transitions, [])
                    for other_state in self.states:
                        if other_state == next_state:
                            next_state = other_state
                            break
                    else:
                        self.add_state(next_state)
                else:
                    next_state = tuple(this_letter_transitions)[0]

                paths += [(letter, next_state)]


class FSMSuperState(FSMState):
    # component_states expected to be a set
    def __init__(self, component_states, edges, id=None, terminal=False):
        super(FSMSuperState, self).__init__(edges, id=id, terminal=terminal)
        self.component_states = component_states

    def __eq__(self, other):
        if type(other) is FSMState:
            if len(self.component_states) == 1:
                return self.component_states[0] == other

        if type(other) is not FSMSuperState:
            return False

        same = True
        for component_state in component_states:
            same = same and (component_state in other.component_states)
