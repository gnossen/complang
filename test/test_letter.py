from letter import *
from letter_string import *
from alphabet import *
from alphabet_union import *
import pytest
import pdb

alpha = alphabet(["A", "B", "C"])
alpha2 = alphabet(["X", "Y", "Z"])
strA = alpha(str="A")
strB = alpha(str="B")
strC = alpha(str="C")

str1 = LetterString(letter_cls=alpha, str="ABC")

def test_equality():
    str2 = alpha(str="A")
    assert strA == str2
    assert strA != strB

    assert strA.id() == 0
    assert strB.id() == 1
    assert strC.id() == 2

def test_equality_not_letter():
    assert strA != 5

def test_equality_str():
    assert strA == "A"

def test_equality_subalphabet():
    alpha12 = alphabet_union(alpha, alpha2)
    strA_prime = alpha12(str="A")
    assert strA == strA_prime
    assert strA_prime == strA

def test_size():
    assert alpha.size() == 3

def test_letter_all():
    assert list(alpha.all()) == [strA, strB, strC]

def test_letter_str():
    s = LetterString(letter_cls=alpha, str="ABC")
    assert str(s) == "ABC"
    assert len(s) == 3
    assert s[0] == alpha(str="A")

def test_embed():
    assert strA.embed() == [1.0, 0.0, 0.0]
    assert strB.embed() == [0.0, 1.0, 0.0]
    assert strC.embed() == [0.0, 0.0, 1.0]

def test_parse_nonletter():
    with pytest.raises(Exception):
        strD = alpha(str="D")

    with pytest.raises(Exception):
        str = LetterString(alpha, str="XYZ")

    with pytest.raises(Exception):
        letter = alpha.from_str("D")

def test_list_alphabet_no_args():
    with pytest.raises(Exception):
        a = alpha()

def test_list_alphabet_is_letter():
    assert alpha.is_letter("A")
    assert not alpha.is_letter("Z")

def test_long_letter_short_string():
    alpha2 = alphabet(["a", "n", "n~"])
    n = LetterString(letter_cls=alpha2, str="n")

def test_letter_string_from_letter_list():
    a = LetterString(letter_list=[strA, strB, strC])
    assert str(a) == "ABC"

def test_letter_string_heterogeneous():
    strX = alpha2(str="X")
    with pytest.raises(Exception):
        s = LetterString(letter_list=[strA, strX])

def test_letter_string_homogeneous():
    alpha1 = alphabet(["A", "B"])
    alpha2 = alphabet(["X", "Y"])
    alpha12 = alphabet_union(alpha1, alpha2)
    letter_str = LetterString(letter_cls=alpha12, str="ABXY")
    for letter in letter_str._letter_list:
        assert letter.__class__ is alpha12

def test_letter_string_no_str_arg():
    s = LetterString(letter_cls=alpha)
    assert len(s._letter_list) == 0

def test_letter_string_no_args():
    with pytest.raises(Exception):
        s = LetterString()

def test_letter_string_equals():
    str2 = LetterString(letter_list=[strA, strB, strC])
    assert str1 == str2

def test_letter_string_not_equals():
    str2 = LetterString(letter_cls=alpha, str="ABA")
    assert str1 != str2

def test_letter_string_index_not_int():
    with pytest.raises(Exception):
        a = str1["a"]

    with pytest.raises(Exception):
        str1["a"] = 2

def test_letter_string_empty_list_no_letter_class():
    with pytest.raises(Exception):
        LetterString(letter_list="")

def test_to_letter():
    alpha3 = alphabet_union(alpha, alpha2)
    A = alpha(str="A")
    A_ = to_letter(A, alpha3)
    assert A_ == A

    with pytest.raises(Exception):
        to_letter(5, alpha)

def test_letter_string_not_equal():
    s = LetterString(letter_cls=alpha, str="ABB")
    assert s != 5

def test_letter_string_iteration():
    s = LetterString(letter_cls=alpha, str="ABC")
    letter_list = []
    for letter in s:
        letter_list.append(str(letter))

    assert letter_list == ["A", "B", "C"]

def test_letter_setitem():
    str1[2] = alpha(str="B")
    assert str(str1) == "ABB"

def test_letter_setitem_as_str():
    str1[2] = "B"
    assert str(str1) == "ABB"

def test_letter_string_set_different_alphabet():
    strX = alpha2(str="X")
    with pytest.raises(Exception):
        str1[1] = strX

def test_letter_string_append():
    str1 = LetterString(letter_cls=alpha, str="AB")
    str1.append(alpha(str="C"))
    assert str(str1) == "ABC"
    str1.append("B")
    assert str(str1) == "ABCB"

def test_letter_string_add():
    str1 = LetterString(letter_cls=alpha, str="ABC")
    str2 = LetterString(letter_cls=alpha, str="CBA")
    assert str(str1 + str2) == "ABCCBA"

def test_letter_string_add_single_letter():
    str1 = LetterString(letter_cls=alpha, str="ABC")
    assert str(str1 + alpha(str="A")) == "ABCA"

def test_letter_string_add_single_ltter():
    str1 = LetterString(letter_cls=alpha, str="ABC")
    assert str(str1 + alpha(str="A")) == "ABCA"

def test_letter_string_add_str():
    str1 = LetterString(letter_cls=alpha, str="ABC")
    assert str(str1 + "AB") == "ABCAB"

def test_letter_string_embed():
    str1 = LetterString(letter_cls=alpha, str="ABC")
    embedded = str1.embed()
    assert embedded == [
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ]

def test_letter_string_wrong_type():
    with pytest.raises(Exception):
        str1 + 5

def test_instantiate_list_alphabet_different_alphabet():
    X = alpha2(str="X")
    with pytest.raises(Exception):
        alpha(letter=X)
    
def test_get_maximal_alphabet():
    letters1 = ["A", "B", "C"]
    alphabet1 = alphabet(letters1)
    letters2 = ["X", "Y", "Z"]
    alphabet2 = alphabet(letters2)
    letters3 = ["1", "2", "3"]
    alphabet3 = alphabet(letters3)
    alphabet12 = alphabet_union(alphabet1, alphabet2)
    alphabet23 = alphabet_union(alphabet2, alphabet3)
    alphabet13 = alphabet_union(alphabet1, alphabet3)
    alphabet123 = alphabet_union(alphabet12, alphabet3)
    classes = [alphabet1, alphabet13, alphabet123]
    maximal = LetterString._get_maximal_alphabet(classes)
    assert maximal.is_subalphabet(alphabet123)
    assert alphabet123.is_subalphabet(maximal)
