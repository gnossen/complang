import pytest
from fsm import FSM
from fsm_state import FSMState
from alphabet import alphabet

Alphabet = alphabet(["A", "B", "C"])

def test_instantiate():
    fsm = FSM(Alphabet)
    assert fsm.states == []
    assert fsm.state_count == 1
    assert fsm.initial_state == None
    assert fsm._letter_cls is Alphabet

    with pytest.raises(Exception):
        fsm.match("")

    assert fsm.get_state(0) is None

    with pytest.raises(Exception):
        fsm._add_state(5)

    state = FSMState()
