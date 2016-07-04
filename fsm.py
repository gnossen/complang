from regexast import *
import pydot
import copy
import pdb

class FSM(object):
    def __init__(self, letter_class):
        self.letter_class = letter_class
        self.initial_state = None
        self.states = []
        self.state_count = 1

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
    def __init__(self, letter_class):
        super(NFSM, self).__init__(letter_class)
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
        self.clear_visited()

    def _connect_dead_state(self, state):
        dead_transitions = set()
        for letter in self.letter_class.all():
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
                print("Removing %d." % state._id)
                self.remove_impossible(state)

    def from_regex(self, ast):
        self.initial_transitions = self._from_regex(ast)
        self.initial_state = FSMState([self.initial_transitions])
        self.add_state(self.initial_state)
        self.connect_dead_state()
        self.reverse_ids()
        self.clear_visited()
        self.remove_impossible_states()
        
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

            if next_transition is not None:
                loop_state.add_edges([loop_init_transition, next_transition])
            else:
                loop_state.add_edges([loop_init_transition])

            self.add_state(loop_state)
            return (-1, loop_state)
        else:
            raise Exception("Unknown AST type.")

class FSMState(object):
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

    def get_epsilon_edges(self):
        epsilon_edges = []
        for letters, next_state in self.edges:
            if len(letters) == 1 and tuple(letters)[0] == -1:
                epsilon_edges += [(letters, next_state)]

        return epsilon_edges

    def get_edges_to(self, state):
        edges_to = []
        for letters, next_state in self.edges:
            if next_state is state:
                edges_to += [(letters, next_state)]

        return edges_to

    def remove_edges_to(self, state):
        self.edges = [edge for edge in self.edges if not edge[1] is state]

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
            letters = letters | transition_letters

        return letters

    def nd_transition(self, letter):
        new_states = set()
        if not self.visited:
            self.visit()
            for edge_letter_set, state in self.edges:
                if letter in edge_letter_set:
                    new_states = new_states | {state}

                if -1 in edge_letter_set:
                    new_states = new_states | state.nd_transition(letter)

        return new_states

    def __eq__(self, other):
        return self._id == other._id

class DFSM(FSM):
    def from_regex(self, ast):
        nfsm = NFSM(self.letter_class)
        nfsm.from_regex(ast)
        nfsm.draw("nfsm-record.png")
        self.from_nfsm(nfsm)

    def from_nfsm(self, nfsm):
        self.dead_state = FSMSuperState({nfsm.dead_state}, [])
        self.add_state(self.dead_state)
        self.initial_state = FSMSuperState({nfsm.initial_state}, [])
        self.add_state(self.initial_state)
        self._from_nfsm(nfsm, self.initial_state)
        self.clear_visited()

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
            self.add_state(ref_state)

        return ref_state

    def _from_nfsm(self, nfsm, state):
        if not state.visited:
            state.visit()
            paths = []

            for letter in self.letter_class.all():
                this_letter_states = state.nd_transition(letter.id(), nfsm)
                next_state = self.make_state(this_letter_states)

                paths += [(letter.id(), next_state)]

            state.add_edges(paths)
            for _, next_state in state.edges:
                self._from_nfsm(nfsm, next_state)


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
            new_states = new_states | component_state.nd_transition(letter_id)
            nfsm.clear_visited()

        return new_states
