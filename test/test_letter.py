from letter import *
from letter_string import *
from alphabet import *
import pytest

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

def test_letter_string_no_args():
    with pytest.raises(Exception):
        s = LetterString(letter_cls=alpha)

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
