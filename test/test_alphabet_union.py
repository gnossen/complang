from alphabet import *
from alphabet_union import *
import pytest

letters1 = ["A", "B", "C"]
alphabet1 = alphabet(letters1)
letters2 = ["X", "Y", "Z"]
alphabet2 = alphabet(letters2)
alphabet3 = alphabet_union(alphabet1, alphabet2)

def test_union_elements():
    assert [str(letter) for letter in alphabet3.all()] == ["A", "B", "C", "X", "Y", "Z"]

def test_instantiate_letter():
    A = alphabet3(letter=alphabet1(str="A"))
    assert str(A) == "A"
    assert A.id() == 0
    X = alphabet3(letter=alphabet2(str="X"))
    assert str(X) == "X"
    assert X.id() == 3

def test_instantiate_non_subalphabet_letter():
    alphabetQ = alphabet(["Q"])
    with pytest.raises(Exception):
        alphabet3(letter=alphabetQ(str="Q"))

def test_instatiate_with_str():
    A = alphabet3(str="A")
    assert str(A) == "A"
    assert A.id() == 0
    X = alphabet3(str="X")
    assert str(X) == "X"
    assert X.id() == 3

def test_instantiate_non_subalphabet_letter_with_str():
    with pytest.raises(Exception):
        alphabet3(str="Q")

def test_instantiate_no_arguments():
    with pytest.raises(Exception):
        alphabet3()

def test_is_letter():
    for letter in letters1:
        assert alphabet3.is_letter(letter)
    for letter in letters2:
        assert alphabet3.is_letter(letter)
    assert not alphabet3.is_letter("Q")

def test_parse_one():
    test_str = "AXB"
    letter, rem = alphabet3.parse_one(test_str)
    assert letter == alphabet1(str="A")
    assert rem == "XB"
    
    letter, rem = alphabet3.parse_one(rem)
    assert letter == alphabet2(str="X")
    assert rem == "B"

def test_parse_one_not_subalphabet():
    test_str = "QAXYZ"
    with pytest.raises(Exception):
        alphabet3.parse_one(test_str)

def test_is_subalphabet():
    assert alphabet3.is_subalphabet(alphabet1)
    assert alphabet3.is_subalphabet(alphabet2)
    alphabetQ = alphabet(["Q"])
    assert not alphabet3.is_subalphabet(alphabetQ)

def test_layers():
    regex_alphabet = alphabet(["(", ")", "*", "|"])
    alphabet4 = alphabet_union(alphabet3, regex_alphabet)
    assert alphabet4.is_subalphabet(alphabet1)
    assert alphabet4.is_subalphabet(alphabet2)
    assert alphabet4.is_subalphabet(regex_alphabet)

def test_parse_one_common_elements():
    alphabetA = alphabet(["n", "a'"])
    alphabetB = alphabet(["n~", "a"])
    alphabetC = alphabet_union(alphabetA, alphabetB)
    test_str = "n~a'"
    letter, rem = alphabetC.parse_one(test_str)
    assert letter == alphabetB(str="n~")
    letter, rem = alphabetC.parse_one(rem)
    assert letter == alphabetA(str="a'")

def test_common_letters():
    alphabet3 = alphabet(["C", "D", "E"])
    with pytest.raises(Exception):
        alphabet_union(alphabet1, alphabet3)
