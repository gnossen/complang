from edge import Edge, EpsilonAlphabet
from alphabet import alphabet
from alphabet_union import alphabet_union
from unittest.mock import MagicMock

LiteralAlphabet = alphabet(["A", "B", "C"])
FSMAlphabet = alphabet_union(LiteralAlphabet, EpsilonAlphabet)
A = FSMAlphabet(str="A") 
B = FSMAlphabet(str="B") 
C = FSMAlphabet(str="C") 
epsilon = FSMAlphabet(str="ε")

def test_initialize():
    next_state = MagicMock()
    edge = Edge([A, B], next_state) 

    assert edge.letters == {A, B}
    assert edge.next_state is next_state

    edge.add_letter(C)
    assert edge.letters == {A, B, C}

def test_is_epsilon():
   state1 = MagicMock() 
   state2 = MagicMock() 
   
   edge1 = Edge([epsilon], state1)
   assert edge1.is_epsilon()

   edge2 = Edge([A, B], state2)
   assert not edge2.is_epsilon()

def test_merge():
    state1 = MagicMock()
    state2 = MagicMock()

    edge1 = Edge([A], state1)
    edge2 = Edge([B], state1)
    edge3 = Edge([B, C], state2)

    merged_edges = Edge.merge([edge1, edge2, edge3])

    assert len(merged_edges) == 2
    merged_edge = [edge for edge in merged_edges if edge.next_state is state1][0]
    unmerged_edge = [edge for edge in merged_edges if edge.next_state is state2][0]

    assert merged_edge.letters == {A, B}
    assert unmerged_edge.letters == {B, C}
