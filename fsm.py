from regex import *
import pydot

class FSM:
    def __init__(self, letter_class):
        self.letter_class = letter_class
        self.initial_state = None
        self.states = []
        self.state_count = 1

    def from_regex(self, ast):
        self.initial_state = self._from_regex(ast)
        self.determinify()

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
                    letter_str_list = [str(self.letter_class(letter_id)) for letter_id in list(transition_set)]
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

    def _from_regex(self, ast, next_state=None):
        if ast.type == RegexASTNode.CAT_EXPR:
            state_B = self._from_regex(ast.right, next_state=None)
            state_A = self._from_regex(ast.left, next_state=state_B)
            return state_A
        elif ast.type == RegexASTNode.LETTER:
            state_B = next_state
            if next_state is None:
                state_B = FSMState(self.state_count, [], terminal=True)
                self.states += [state_B]
                self.state_count += 1

            state_A = FSMState(self.state_count, [(ast.value.id(), state_B)])
            self.states += [state_A]
            self.state_count += 1
            return state_A
        elif ast.type == RegexASTNode.EPSILON:
            state_B = next_state
            if next_state is None:
                state_B = FSMState(self.state_count, [], terminal=True)
                self.states += [state_B]
                self.state_count += 1

            state_A = FSMState(self.state_count, [(-1, state_B)])
            self.states += [state_A]
            self.state_count += 1
            return state_A
        elif ast.type == RegexASTNode.OR_EXPR:
            transitions_B = self._find_initial_letters(ast.left)
            state_B = self._from_regex(ast.left, next_state=next_state)

            transitions_C = self._find_initial_letters(ast.right)
            state_C = self._from_regex(ast.right, next_state=next_state)

            transitions = [(transitions_B, state_B), (transitions_C, state_C)]
            state_A = FSMState(self.state_count, transitions)
            self.states += [state_A]
            self.state_count += 1
            return state_A
        elif ast.type == RegexASTNode.REP_EXPR:
            state_A = FSMState(self.state_count, [])
            self.states += [state_A]
            self.state_count += 1
            state_B = self._from_regex(ast.left, next_state=state_A)

            transitions = [(self._find_initial_letters(ast.left), state_B)]
            state_A.set_edges(transitions)
            return state_A
        else:
            raise Exception("Unknown AST type.")

    def _find_initial_letters(self, ast):
        if ast.type == RegexASTNode.CAT_EXPR:
            return self._find_initial_letters(ast.left)
        elif ast.type == RegexASTNode.EPSILON:
            return {-1}
        elif ast.type == RegexASTNode.LETTER:
            return {ast.value.id()}
        elif ast.type == RegexASTNode.OR_EXPR:
            return self._find_initial_letters(ast.left) | \
                    self._find_initial_letters(ast.right)
        elif ast.type == RegexASTNode.REP_EXPR:
            return self._find_initial_letters(ast.left)
        else:
            raise Exception("Unknown AST type.")

    def determinify(self):
        pass

class FSMState:
    def __init__(self, id, edges, terminal=False):
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

