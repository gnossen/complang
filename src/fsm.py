from regexast import *
from letter_string import LetterString, to_letter_string
from fsm_state import FSMState
from contextlib import contextmanager
import pydot
import copy

class FSM():
    def __init__(self, letter_cls):
        self._letter_cls = letter_cls
        self.initial_state = None
        self.states = []
        self.state_count = 1

    def match(self, letter_str):
        if self.initial_state is None:
            raise Exception("Cannot match against uninitialized FSM.")
        
        letter_str = to_letter_str(letter_str, self._letter_cls)
        state = self.initial_state
        for letter in letter_list:
            state = state.transition(letter)
            if state is None:
                return False

        return state.terminal

    def get_state(self, id):
        for state in self.states:
            if state._id == id:
                return state
        else:
            return None

    def _clear_visited(self):
        for state in self.states:
            state._clear_visited()

    def _add_state(self, state):
        if not isinstance(state, FSMState):
            raise Exception("State must be an instance of FSMState")

        state._id = self.state_count
        self.state_count += 1
        self.states += [state]

    @contextmanager
    def traverse(self):
        self._clear_visited()
        yield
        self._clear_visited()

    def draw(self, filename, show_dead=False): # pragma: no cover
        graph = pydot2.Dot(graph_type='digraph')
        state_hash = {}
        def _draw(state):
            if not state.visited:
                node = pydot2.Node(str(state._id), label=('"%s"' % str(state._id)))
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
                                letter_str_list += [str(self._letter_cls(letter_id))]

                        edge_label = '"' +  ", ".join(letter_str_list) + '"'
                        graph_edge = pydot2.Edge(node, new_node) 
                        graph_edge.set_label(edge_label)
                        graph.add_edge(graph_edge)

                return node
            else:
                return state_hash[state]

        _draw(self.initial_state)
        graph.write_png(filename)
        self._clear_visited()
