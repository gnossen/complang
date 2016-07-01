from regex import *
import pydot

class FSM:
    def __init__(self, letter_class):
        self.letter_class = letter_class
        self.initial_state = None
        self.states = []
        self.state_count = 1

    def clear_visited(self):
        for state in self.states:
            state.clear_visited()

    def draw(self, filename):
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

    def add_state(self, state):
        state._id = self.state_count
        self.state_count += 1
        self.states += [state]

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
        self.determinify()

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
            self.add_state(loop_state)
            loop_init_transition = self._from_regex(ast.left, next_transition=(-1, loop_state))
            loop_state.set_edges([loop_init_transition, next_transition])
            return (-1, loop_state)
        else:
            raise Exception("Unknown AST type.")

    def determinify(self):
        pass

class FSMState:
    def __init__(self, edges, id=None, terminal=False):
        # edges is expected to be of the form
        #    [ ({letter1_id1, letter1_id2}, new_state1), ... , (lettern_id, new_staten)]
        self.edges = []
        self._id = id
        self.set_edges(edges)
        self.visited = False

        self.terminal = terminal

    def __hash__(self):
        return hash(self._id)

    def clear_visited(self):
        self.visited = False

    def visit(self):
        self.visited = True

    def set_edges(self, edges):
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

    def nondeterministic_transition(self, letter):
        new_states = set()
        for edge_letter_set, state in self.edges:
            if letter in edge_letter_set:
                new_states = new_states | {state}

            if -1 in edge_letter_set:
                new_states = new_states | state.nondeterministic_transition()

        return new_states

