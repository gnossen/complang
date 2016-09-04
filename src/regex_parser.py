from letter import *
from letter_string import *
from regexast import *
from alphabet import *

RegexAlphabet = alphabet(["(", ")", "*", "|", "0"])

class RegexParser:
    def __init__(self, letter_str):
        self._stream = letter_str
        self._letter_cls = letter_str[0].__class__
        self._stream_index = 0

    def parse(self):
        return self._parse_body()

    def _check(self, letter):
        return self._head() == letter

    def _head(self):
        return None if len(self._stream) == 0 else self._stream[0]

    def _match(self, letter):
        if not self._check(letter):
            head_letter = self._head()
            raise Exception("Expected %s but encountered %s! (%d)" %
                    (str(letter), str(self._head(), self._stream_index))) 

        self._advance()

    def _advance(self):
        self._stream = self._stream[1:]
        self._stream_index += 1

    def _parse_body(self):
        return self._parse_expr()

    def _parse_expr(self):
        left = self._parse_expr2()

        if self._check(RegexAlphabet(str="|")):
            self._match(RegexAlphabet(str="|"))
            right = self._parse_expr()
            return RegexASTNode(RegexASTNode.OR_EXPR, self._letter_cls, left=left, right=right)

        return left

    def _check_expr2(self):
        return self._check_expr3()

    def _parse_expr2(self):
        left = self._parse_expr3()
        if self._check_expr2():
            right = self._parse_expr2()
            return RegexASTNode(RegexASTNode.CAT_EXPR, self._letter_cls, left=left, right=right)

        return left

    def _check_expr3(self):
        return self._check_expr4()

    def _parse_expr3(self):
        subtree = self._parse_expr4()
        
        while self._check(RegexAlphabet(str="*")):
            self._match(RegexAlphabet(str="*"))
            subtree = RegexASTNode(RegexASTNode.REP_EXPR, self._letter_cls, left=subtree)

        return subtree

    def _check_expr4(self):
        return self._head() is not None and \
                not self._check(RegexAlphabet(str=")")) and \
                not self._check(RegexAlphabet(str="*")) and \
                not self._check(RegexAlphabet(str="|"))

    def _parse_expr4(self):
        if self._check(RegexAlphabet(str="0")):
            self._match(RegexAlphabet(str="0"))
            return RegexASTNode(RegexASTNode.EPSILON, self._letter_cls)
        elif self._check(RegexAlphabet(str="(")):
            self._match(RegexAlphabet(str="("))
            expr = self._parse_expr()
            self._match(RegexAlphabet(str=")"))
            return expr
        else:
            letter = self._head()
            self._advance()
            return RegexASTNode(RegexASTNode.LETTER, self._letter_cls, value=letter)
