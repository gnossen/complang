from alphabet import *
from regexast import *

Alphabet = alphabet(["A", "B", "C"])

def test_instantiate_node():
    letter = Alphabet(str="A")
    node = RegexASTNode(RegexASTNode.LETTER, Alphabet, value=letter)
    assert str(node) == "A"

def test_to_letter_string():
    # (A|B)(BC)*
    node8 = RegexASTNode(RegexASTNode.LETTER, Alphabet, value=Alphabet(str="C"))
    node7 = RegexASTNode(RegexASTNode.LETTER, Alphabet, value=Alphabet(str="B"))
    node6 = RegexASTNode(RegexASTNode.CAT_EXPR, Alphabet, left=node7, right=node8)
    node5 = RegexASTNode(RegexASTNode.REP_EXPR, Alphabet, left=node6)
    node4 = RegexASTNode(RegexASTNode.LETTER, Alphabet, value=Alphabet(str="B"))
    node3 = RegexASTNode(RegexASTNode.LETTER, Alphabet, value=Alphabet(str="A"))
    node2 = RegexASTNode(RegexASTNode.OR_EXPR, Alphabet, left=node3, right=node4)
    node1 = RegexASTNode(RegexASTNode.CAT_EXPR, Alphabet, left=node2, right=node5)
    assert node1.to_letter_string() == "(A|B)(BC)*"

def test_render_epsilon():
    node = RegexASTNode(RegexASTNode.EPSILON, Alphabet)
    assert node.to_letter_string() == "0"

def test_embed():
    node = RegexASTNode(RegexASTNode.LETTER, Alphabet, value=Alphabet(str="A"))
    assert node.embed() == [[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    
