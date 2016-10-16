from fsm_state import FSMState
from edge import Edge, EpsilonAlphabet
from alphabet_union import alphabet_union
from unittest.mock import MagicMock
import pytest
import pdb

edges = [MagicMock(), MagicMock()]

@pytest.yield_fixture()
def edge_merge():
    old_merge = Edge.merge
    Edge.merge = MagicMock()
    yield Edge.merge
    Edge.merge = old_merge

def test_instantiate():
    state = FSMState(edges)

    assert state.edges == edges
    assert state._id is None
    assert state.visited == False
    assert state.terminal == False

    state2 = FSMState(edges, id=1, terminal=True)

    assert state2.edges == edges
    assert state2._id is 1
    assert state2.visited == False
    assert state2.terminal == True

def test_visit():
    state = FSMState(edges)

    assert not state.visited
    state.visit()
    assert state.visited
    state._clear_visited()
    assert not state.visited

def test_get_epsilon_edges():
    edge1 = MagicMock()
    edge1.is_epsilon.return_value = True
    edge2 = MagicMock()
    edge2.is_epsilon.return_value = False

    edges = [edge1, edge2]
    state = FSMState(edges)

    assert state.get_epsilon_edges() == [edge1]

def test_get_edges_to():
    state1 = MagicMock()
    state2 = MagicMock()

    edge1 = MagicMock()
    edge1.next_state = state1
    edge2 = MagicMock()
    edge2.next_state = state2

    edges = [edge1, edge2]

    state = FSMState(edges)
    assert state.get_edges_to(state1) == [edge1]

def test_add_edges(edge_merge):
    edge1 = MagicMock()
    edge2 = MagicMock()
    edges = [edge1, edge2]
    edge_merge.return_value = [edge1, edge2]
    state = FSMState(edges)
    edge_merge.assert_called_with([edge1, edge2]) 

    edge3 = MagicMock()
    state.add_edges([edge3])
    edge_merge.assert_called_with([edge1, edge2, edge3]) 

def test_hash():
    state = FSMState([], id=2)
    assert state.__hash__() == hash(2)

def test_remove_edges_to():
    edge1 = MagicMock()
    state1 = MagicMock()
    edge1.next_state = state1
    edge2 = MagicMock()
    state2 = MagicMock()
    edge2.next_state = state2
    edge3 = MagicMock()
    state3 = MagicMock()
    edge3.next_state = state3

    edges = [edge1, edge2, edge3]
    state = FSMState(edges) 
    assert state.edges == edges
    state.remove_edges_to(state1)
    assert state.edges == [edge2, edge3]

def test_transition():
    letter1 = MagicMock()
    letter2 = MagicMock()
    state1 = MagicMock()
    edge1 = MagicMock()
    edge1.letters = {letter1, letter2}
    edge1.next_state = state1
    letter3 = MagicMock()
    state2 = MagicMock()
    edge2 = MagicMock()
    edge2.letters = {letter3}
    edge2.next_state = state2

    edges = [edge1, edge2]
    state = FSMState(edges)
    assert state.transition(letter1) is state1
    assert state.transition(letter2) is state1
    assert state.transition(letter3) is state2

    letter4 = MagicMock()
    assert state.transition(letter4) is None

    assert state.valid_transitions() == {letter1, letter2, letter3}

    # base cases in which the results are equivalent to state.transition
    state.visited = False
    assert state.nd_transition(letter1) == {state1}
    state.visited = False
    assert state.nd_transition(letter2) == {state1}
    state.visited = False
    assert state.nd_transition(letter3) == {state2}

    edge3 = MagicMock()
    edge3.letters = {letter1, letter4}
    state3 = MagicMock()
    edge3.next_state = state3

    # case which returns more than one state
    state.add_edges([edge3])
    
    state.visited = False
    assert state.nd_transition(letter1) == {state1, state3}

    # recursive case -- epsilon edges
    edge4 = MagicMock()
    edge4.letters = [EpsilonAlphabet(str="ε")]

    edge5 = MagicMock()
    edge5.letters = [letter1]
    edge5.next_state = state
    state4 = FSMState([edge5])
    state.add_edges([edge4])

    state.visited = False
    assert state.nd_transition(letter1) == {state1, state3, state}
