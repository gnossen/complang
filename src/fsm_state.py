from edge import Edge, EpsilonAlphabet

class FSMState:
    def __init__(self, edges, id=None, terminal=False):
        self.edges = []
        self._id = id
        self.add_edges(edges)
        self.visited = False

        self.terminal = terminal

    def __hash__(self):
        return hash(self._id)

    def _clear_visited(self):
        self.visited = False

    def visit(self):
        self.visited = True

    def get_epsilon_edges(self):
        return [edge for edge in self.edges if edge.is_epsilon()]

    def get_edges_to(self, state):
        return [edge for edge in self.edges if edge.next_state is state]

    def remove_edges_to(self, state):
        self.edges = [edge for edge in self.edges if edge.next_state is not state]

    def add_edges(self, edges):
        self.edges += edges
        self.edges = Edge.merge(self.edges)

    # only call on deterministic nodes
    def transition(self, letter):
        for edge in self.edges:
            if letter in edge.letters:
                return edge.next_state
        return None

    def valid_transitions(self):
        letters = set()
        for edge in self.edges:
            letters = letters | edge.letters

        return letters

    def nd_transition(self, letter):
        new_states = set()
        if not self.visited:
            self.visit()
            for edge in self.edges:
                if letter in edge.letters:
                    new_states = new_states | {edge.next_state}

                if EpsilonAlphabet(str="ε") in edge.letters:
                    new_states = new_states | edge.next_state.nd_transition(letter)

        return new_states

    def __eq__(self, other):
        return self._id == other._id
