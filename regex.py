from letter import *
import random
import math
import numpy

# note that at the moment, this parser only works for articulatory spaces in which
# there is a one-to-one correspondence between letters and characters
# So, for example, diacritics will not work at the moment.


class Regex:
    def __init__(self, letter_class):
        random.seed()
        self.letter_class = letter_class
        self.ast = None

    def embed(self):
        return self.ast.embed()

    def generate_regex(self):
        self.ast = self._generate_regex(1)

    def _generate_regex(self, depth):
        # calculate mean length for this particular depth
        mean_layer_length = 6.0 / (depth ** 2)
        layer_length = math.floor(random.gauss(mean_layer_length, 2))
        layer_length = 1 if layer_length < 1 else layer_length

        res = []
        for i in range(layer_length):
            c = random.random()

            # 80% chance it's a letter
            if c < 0.75:
                letter_index = random.randrange(self.letter_class.size())
                res += [ RegexASTNode(RegexASTNode.LETTER, self.letter_class, value=self.letter_class(letter_index)) ]
            elif c < 0.85:
                left = self._generate_regex(depth + 1)
                right = self._generate_regex(depth + 1)
                res += [ RegexASTNode(RegexASTNode.OR_EXPR, self.letter_class, left=left, right=right) ]
            else:
                expr = self._generate_regex(depth + 1)
                res += [ RegexASTNode(RegexASTNode.REP_EXPR, self.letter_class, left=expr) ]

        def simplify(sublist):
            for elem in sublist:
                if elem.type == RegexASTNode.REP_EXPR and \
                    elem.left.type == RegexASTNode.REP_EXPR:

                    elem.left = elem.left.left

            return sublist

        def treeify(sublist):
            if len(sublist) == 1:
                return sublist[0]
            else:
                return RegexASTNode(RegexASTNode.CAT_EXPR,
                                    self.letter_class,
                                    left=sublist[0],
                                    right=treeify(sublist[1:]))
         
        return treeify(simplify(res))


    def generate(self):
        return self._generate(self.ast)

    def _generate(self, ast):
        if ast is None:
            return []
        elif ast.type == RegexASTNode.EPSILON:
            return []
        elif ast.type == RegexASTNode.LETTER:
            return [ ast.value ]
        elif ast.type == RegexASTNode.OR_EXPR:
            choice = random.randrange(2)
            if choice == 0:
                return self._generate(ast.left)
            else:
                return self._generate(ast.right)
        elif ast.type == RegexASTNode.REP_EXPR:
            num_reps = math.floor(random.gauss(5, 2))
            if num_reps < 0:
                num_reps = 0

            res = []
            for i in range(num_reps):
                res += self._generate(ast.left)

            return res
        elif ast.type == RegexASTNode.CAT_EXPR:
            return self._generate(ast.left) + self._generate(ast.right)
        else:
            raise Exception("What the fuck is %s!?" % ast)

    def head(self):
        return "" if len(self.in_stream) == 0 else self.in_stream[0]

    def match(self, str):
        if not self.check(str):
            head_letter = "EOF" if len(self.in_stream) == 0 else self.in_stream[0]
            raise Exception("Expected %s but encountered %s! (%d)" % (str, head_letter, self.in_stream_index))

        self.advance()
        return True

    def check(self, str):
        if str == None:
            return len(self.in_stream) == 0

        return self.head() == str

    def advance(self):
        self.in_stream_index += 1
        self.in_stream = self.in_stream[1:]

    def from_embedding(self, embed_stream):
        def embedding_to_index(embedding):
            return numpy.argmax(embedding)

        def index_to_str(index):
            if index == RegexASTNode.EPSILON_VECINDEX:
                return "0"
            elif index == RegexASTNode.OR_VECINDEX:
                return "|"
            elif index == RegexASTNode.LPAREN_VECINDEX:
                return "("
            elif index == RegexASTNode.RPAREN_VECINDEX:
                return ")"
            elif index == RegexASTNode.STAR_VECINDEX:
                return "*"
            else:
                return str(self.letter_class(index - RegexASTNode.NUM_RESERVED_SYMBOLS))

        res = ""
        for embedding in embed_stream:
            res += index_to_str(embedding_to_index(embedding))

        self.parse(res)

    def __repr__(self):
        if self.ast is None:
            return "<Uninitialized Regex>"
        else:
            return str(self.ast)

    __str__ = __repr__

    def parse(self, str):
        print("Parsing '%s'" % str)
        self.in_stream = str
        self.in_stream_index = 0
        self.ast = self.parse_body()

    def parse_body(self):
        left = self.parse_expr()
        if self.check_expr():
            right = self.parse_expr()
            return RegexASTNode(RegexASTNode.CAT_EXPR, self.letter_class, left=left, right=right)
        else:
            return left
            
    def check_expr(self):
        return self.check("0") or self.check_expr2()

    def parse_expr(self):
        left_expr = None
        if self.check("0"):
            self.match("0")
            left_expr = RegexASTNode(RegexASTNode.EPSILON, self.letter_class)
        else:
            left_expr = self.parse_expr2()

        if self.check("|"):
            self.match("|")
            right_expr = self.parse_body()
            return RegexASTNode(RegexASTNode.OR_EXPR, self.letter_class, left=left_expr, right=right_expr)
        else:
            return left_expr

    def check_expr2(self):
        return self.letter_class.is_letter(self.head()) or \
                self.check("(")

    def parse_expr2(self):
        if self.check("("):
            self.match("(")
            expr = self.parse_body()
            self.match(")")
            return expr
        elif self.letter_class.is_letter(self.head()):
            letter = self.letter_class.from_str(self.head())
            self.advance()
            letter_node = RegexASTNode(RegexASTNode.LETTER, self.letter_class, value=letter)

            if self.check("*"):
                self.match("*")
                return RegexASTNode(RegexASTNode.REP_EXPR, self.letter_class, left=letter_node)
            else:
                return letter_node
        else:
            raise Exception("Could not parse '%s' as part of expr2. (%d)" % (self.head(), self.in_stream_index))
       
class RegexASTNode:
    EPSILON     = 0
    LETTER      = 1
    OR_EXPR     = 2
    REP_EXPR    = 3
    CAT_EXPR    = 4

    NUM_RESERVED_SYMBOLS = 5

    EPSILON_VECINDEX    = 0
    OR_VECINDEX         = 1
    LPAREN_VECINDEX     = 2
    RPAREN_VECINDEX     = 3
    STAR_VECINDEX       = 4

    def __init__(self, _type, letter_class, left=None, right=None, value=None):
        self.type = _type
        self.left = left
        self.right = right
        self.value = value
        self.letter_class = letter_class

    def __repr__(self):
        if self.type == RegexASTNode.EPSILON:
            return "0"
        elif self.type == RegexASTNode.LETTER:
            return str(self.value)
        elif self.type == RegexASTNode.OR_EXPR:
            return str(self.left) + "|" + str(self.right)
        elif self.type == RegexASTNode.REP_EXPR:
            if self.left.type == RegexASTNode.CAT_EXPR:
                return "(" + str(self.left) + ")*"
            else:
                return str(self.left) + "*"
        elif self.type == RegexASTNode.CAT_EXPR:
            def parenthesize(subtree):
                if subtree.type == RegexASTNode.OR_EXPR:
                    return "(" + str(subtree) + ")"
                else:
                    return str(subtree)

            return parenthesize(self.left) + parenthesize(self.right)
        else:
            raise Exception("Cannot print AST node of type '%d'." % self.type)

    def embed_by_index(self, index):
        num_elems = RegexASTNode.NUM_RESERVED_SYMBOLS + self.letter_class.size()
        head = [0.0] * index
        middle = [1.0]
        tail = [0.0] * (num_elems - index - 1) 

        return head + middle + tail

    def embed_single(self, char):
        if char == "0":
            return self.embed_by_index(RegexASTNode.EPSILON_VECINDEX)
        elif char == "|":
            return self.embed_by_index(RegexASTNode.OR_VECINDEX)
        elif char == "(":
            return self.embed_by_index(RegexASTNode.LPAREN_VECINDEX)
        elif char == ")":
            return self.embed_by_index(RegexASTNode.RPAREN_VECINDEX)
        elif char == "*":
            return self.embed_by_index(RegexASTNode.STAR_VECINDEX)
        else:
            return self.embed_by_index(self.letter_class.from_str(char).id() + RegexASTNode.NUM_RESERVED_SYMBOLS)

    def embed_from_str(self, str):
        return [ self.embed_single(char) for char in str]

    def embed(self):
        return self.embed_from_str(str(self))
