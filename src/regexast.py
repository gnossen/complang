from pydot import *
from letter_string import *
from alphabet_union import *
from alphabet import *
import uuid

RegexAlphabet = alphabet(["(", ")", "*", "|", "0"])

class RegexASTNode:
    EPSILON     = 0
    LETTER      = 1
    OR_EXPR     = 2
    REP_EXPR    = 3
    CAT_EXPR    = 4

    def __init__(self, _type, letter_cls, left=None, right=None, value=None):
        self.type = _type
        self.left = left
        self.right = right
        self.value = value
        self._letter_cls = alphabet_union(letter_cls, RegexAlphabet)

    def _parenthesize(self, expr):
        buf = LetterString(letter_cls=self._letter_cls)
        buf += "("
        buf += expr
        buf += ")"
        return buf

    def _parenthesize_expr(self, expr):
        if len(expr) == 1:
            return expr

        return self._parenthesize(expr)

    def to_letter_string(self):
        if self.type == RegexASTNode.EPSILON:
            return LetterString(letter_cls=self._letter_cls, str="0")
        elif self.type == RegexASTNode.OR_EXPR:
            return self._parenthesize_expr(self.left.to_letter_string()) + "|" + \
                    self._parenthesize_expr(self.right.to_letter_string())
        elif self.type == RegexASTNode.REP_EXPR:
            return self._parenthesize_expr(self.left.to_letter_string()) + "*"
        elif self.type == RegexASTNode.CAT_EXPR:
            def or_parenthesize(subtree):
                if subtree.type == RegexASTNode.OR_EXPR:
                    return self._parenthesize(subtree.to_letter_string())
                else:
                    return subtree.to_letter_string()
            return or_parenthesize(self.left) + or_parenthesize(self.right)
        elif self.type == RegexASTNode.LETTER:
            return LetterString(letter_list=[self._letter_cls(letter=self.value)])

    def __repr__(self):
        return str(self.to_letter_string())

    __str__ = __repr__

    def embed(self):
        return self.to_letter_string().embed()

    def draw(self, filename): # pragma: no cover
        graph = pydot.Dot(graph_type='digraph')

        def _draw(subtree):
            label = "???"
            if self.type == RegexASTNode.EPSILON:
                label = "0"
            elif self.type == RegexASTNode.LETTER:
                label = str(self.value)
            elif self.type == RegexASTNode.OR_EXPR:
                label = "OR"
            elif self.type == RegexASTNode.REP_EXPR:
                label = "REP"
            elif self.type == RegexASTNode.CAT_EXPR:
                label = "CAT"
                
            node = pydot.Node(str(uuid.uuid1()), label=label) 
            graph.add_node(node)
            
            if subtree.left is not None:
                left = _draw(subtree.left)
                graph.add_edge(pydot.Edge(node, left))

            if subtree.right is not None:
                right = _draw(subtree.right)
                graph.add_edge(pydot.Edge(node, right))

            return node

        _draw(self)
        graph.write_png(filename)
