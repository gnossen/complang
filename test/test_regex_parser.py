import pytest
from letter import *
from regex_parser import *
from letter_string import *
from alphabet import *
from alphabet_union import *

alpha1 = alphabet(["A", "B", "C"])
regex_alphabet = alphabet_union(alpha1, RegexAlphabet)

def test_initialize_regex_parser():
    parser = RegexParser(LetterString(letter_cls=regex_alphabet, str="(ABC)*|(BCA)*"))
    ast = parser.parse()
    assert ast.type == RegexASTNode.OR_EXPR
    assert ast.left.type == RegexASTNode.REP_EXPR
    assert ast.left.left.type == RegexASTNode.CAT_EXPR
    assert ast.left.left.left.type == RegexASTNode.LETTER
    assert ast.left.left.left.value == regex_alphabet(str="A")
    assert ast.left.left.right.type == RegexASTNode.CAT_EXPR
    assert ast.left.left.right.left.type == RegexASTNode.LETTER
    assert ast.left.left.right.left.value == regex_alphabet(str="B")
    assert ast.left.left.right.right.type == RegexASTNode.LETTER
    assert ast.left.left.right.right.value == regex_alphabet(str="C")
    assert ast.right.type == RegexASTNode.REP_EXPR
    assert ast.right.left.type == RegexASTNode.CAT_EXPR
    assert ast.right.left.left.type == RegexASTNode.LETTER
    assert ast.right.left.left.value == regex_alphabet(str="B")
    assert ast.right.left.right.type == RegexASTNode.CAT_EXPR
    assert ast.right.left.right.left.type == RegexASTNode.LETTER
    assert ast.right.left.right.left.value == regex_alphabet(str="C")
    assert ast.right.left.right.right.type == RegexASTNode.LETTER
    assert ast.right.left.right.right.value == regex_alphabet(str="A")

def test_bad_regex():
    with pytest.raises(Exception):
        parser = RegexParser(LetterString(letter_cls=regex_alphabet, str="(ABC"))
        parser.parse()

def test_epsilon():
    parser = RegexParser(LetterString(letter_cls=regex_alphabet, str="A|0"))
    ast = parser.parse()
    assert ast.type == RegexASTNode.OR_EXPR
    assert ast.left.type == RegexASTNode.LETTER
    assert ast.left.value == regex_alphabet(str="A")
    assert ast.right.type == RegexASTNode.EPSILON
