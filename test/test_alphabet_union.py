from alphabet import *
from alphabet_union import *
import pytest

letters1 = ["A", "B", "C"]
alphabet1 = alphabet(letters1)
letters2 = ["X", "Y", "Z"]
alphabet2 = alphabet(letters2)
letters3 = ["1", "2", "3"]
alphabet3 = alphabet(letters3)
alphabet12 = alphabet_union(alphabet1, alphabet2)
alphabet23 = alphabet_union(alphabet2, alphabet3)
alphabet13 = alphabet_union(alphabet1, alphabet3)
alphabet12_13 = alphabet_union(alphabet12, alphabet13)
alphabet12_3 = alphabet_union(alphabet12, alphabet3)


def test_copy_constructor():
    letter = alphabet12(str="A")
    letter2 = alphabet12(letter=letter)
    assert str(letter2) == "A"

def test_equality():
    assert alphabet1(str="A") == alphabet12(str="A")
    assert alphabet2(str="X") == alphabet12(str="X")

def test_union_elements():
    assert [str(letter) for letter in alphabet12.all()] == ["A", "B", "C", "X", "Y", "Z"]

def test_instantiate_letter():
    A = alphabet12(letter=alphabet1(str="A"))
    assert str(A) == "A"
    assert A.id() == 0
    X = alphabet12(letter=alphabet2(str="X"))
    assert str(X) == "X"
    assert X.id() == 3

def test_instantiate_non_subalphabet_letter():
    alphabetQ = alphabet(["Q"])
    with pytest.raises(Exception):
        alphabet12(letter=alphabetQ(str="Q"))

def test_instatiate_with_str():
    A = alphabet12(str="A")
    assert str(A) == "A"
    assert A.id() == 0
    X = alphabet12(str="X")
    assert str(X) == "X"
    assert X.id() == 3

def test_instantiate_non_subalphabet_letter_with_str():
    with pytest.raises(Exception):
        alphabet12(str="Q")

def test_subalphabet_components():
    assert alphabet12_3.is_subalphabet(alphabet13)

def test_instantiate_no_arguments():
    with pytest.raises(Exception):
        alphabet12()

def test_is_letter():
    for letter in letters1:
        assert alphabet12.is_letter(letter)
    for letter in letters2:
        assert alphabet12.is_letter(letter)
    assert not alphabet12.is_letter("Q")

def test_parse_one():
    test_str = "AXB"
    letter, rem = alphabet12.parse_one(test_str)
    assert letter == alphabet1(str="A")
    assert rem == "XB"
    
    letter, rem = alphabet12.parse_one(rem)
    assert letter == alphabet2(str="X")
    assert rem == "B"

def test_parse_one_not_subalphabet():
    test_str = "QAXYZ"
    with pytest.raises(Exception):
        alphabet12.parse_one(test_str)

def test_is_subalphabet():
    assert alphabet12.is_subalphabet(alphabet1)
    assert alphabet12.is_subalphabet(alphabet2)
    alphabetQ = alphabet(["Q"])
    assert not alphabet12.is_subalphabet(alphabetQ)

def test_layers():
    regex_alphabet = alphabet(["(", ")", "*", "|"])
    alphabet4 = alphabet_union(alphabet12, regex_alphabet)
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
    alphabet12 = alphabet(["C", "D", "E"])
    with pytest.raises(Exception):
        alphabet_union(alphabet1, alphabet12)

def test_union_same_alphabet():
    assert alphabet_union(alphabet1, alphabet1) is alphabet1
    assert alphabet_union(alphabet1, alphabet12) is alphabet12
