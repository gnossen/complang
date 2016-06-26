from letter import *

# note that at the moment, this parser only works for articulatory spaces in which
# there is a one-to-one correspondence between letters and characters
# So, for example, diacritics will not work at the moment.


class Regex:
    def __init__(self, letter_class):
        self.letter_class = letter_class

    def head(self):
        return "" if len(self.in_stream) == 0 else self.in_stream[0]

    def match(self, str):
        if not self.check(str):
            head_letter = "EOF" if len(self.in_stream) == 0 else self.in_stream[0]
            raise Exception("Expected %s but encountered %s!" % (str, head_letter))

        self.advance()
        return True

    def check(self, str):
        if str == None:
            return len(self.in_stream) == 0

        return self.head() == str

    def advance(self):
        self.in_stream = self.in_stream[1:]

    def parse(self, str):
        self.in_stream = str
        self.ast = self.parse_body()

    def parse_body(self):
        if self.check(None):
            self.match(None)
            return None
        else:
            left_expr = self.parse_expr()
            if self.check(None):
                return left_expr

            right_expr = self.parse_body()
            return RegexASTNode(RegexASTNode.CAT_EXPR, left=left_expr, right=right_expr)
            
    def check_expr(self):
        return self.check("0") or self.check_expr2()

    def parse_expr(self):
        left_expr = None
        if self.check("0"):
            self.match("0")
            left_expr = RegexASTNode(RegexASTNode.EPSILON)
        else:
            left_expr = self.parse_expr2()

        if self.check("|"):
            self.match("|")
            right_expr = self.parse_expr()
            return RegexASTNode(RegexASTNode.OR_EXPR, left=left_expr, right=right_expr)
        else:
            return left_expr

    def check_expr2(self):
        return self.letter_class.is_letter(self.head()) or \
                self.check("(")

    def parse_expr2(self):
        if self.check("("):
            self.match("(")
            expr = self.parse_expr()
            self.match(")")
            return expr
        elif self.letter_class.is_letter(self.head()):
            letter = self.letter_class.from_str(self.head())
            self.advance()
            letter_node = RegexASTNode(RegexASTNode.LETTER, value=letter)

            if self.check("*"):
                self.match("*")
                return RegexASTNode(RegexASTNode.REP_EXPR, left=letter_node)
            else:
                return letter_node
        else:
            raise Exception("Could not parse %s as part of expr2." % self.head())
       
class RegexASTNode:
    EPSILON     = 0
    LETTER      = 1
    OR_EXPR     = 2
    REP_EXPR    = 3
    CAT_EXPR    = 4

    def __init__(self, _type, left=None, right=None, value=None):
        self.type = _type
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        if self.type == RegexASTNode.EPSILON:
            return "0"
        elif self.type == RegexASTNode.LETTER:
            return str(self.value)
        elif self.type == RegexASTNode.OR_EXPR:
            return "(" + str(self.left) + "|" + str(self.right) + ")"
        elif self.type == RegexASTNode.REP_EXPR:
            return str(self.left) + "*"
        elif self.type == RegexASTNode.CAT_EXPR:
            return str(self.left) + str(self.right)
        else:
            raise Exception("Cannot print AST node of type '%d'." % self.type)
