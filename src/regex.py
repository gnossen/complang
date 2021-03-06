from letter import *
from regexast import *
from fsm import *
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
        self.fsm = None

    def match_str(self, str):
        letter_list = self.letter_class.parse(str)
        return self.fsm.match(letter_list)

    def generate_fsm(self):
        self.fsm = DFSM(self.letter_class)
        self.fsm.from_regex(self.ast)
        return self.fsm

    def embed(self):
        return self.ast.embed()

    def generate_regex(self):
        self.ast = self._generate_regex(1)
        self.generate_fsm()

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
            for i, _ in enumerate(sublist):
                if sublist[i].type == RegexASTNode.REP_EXPR and \
                    sublist[i].left.type == RegexASTNode.REP_EXPR:
                    
                    sublist[i].left = sublist[i].left.left

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
        self.generate_fsm()

    def __repr__(self):
        if self.ast is None:
            return "<Uninitialized Regex>"
        else:
            return str(self.ast)

    __str__ = __repr__

    def parse(self, str):
        self.in_stream = str
        self.in_stream_index = 0
        self.ast = self.parse_body()
        self.generate_fsm()

    def parse_body(self):
        if self.check(None):
            return None

        return self.parse_expr()

    def check_expr(self):
        return self.check_expr2()

    def parse_expr(self):
        left = self.parse_expr2()

        if self.check("|"):
            self.match("|")
            right = self.parse_expr()
            return RegexASTNode(RegexASTNode.OR_EXPR, self.letter_class, left=left, right=right)

        return left

    def check_expr2(self):
        return self.check_expr3()

    def parse_expr2(self):
        left = self.parse_expr3()
        if self.check_expr2():
            right = self.parse_expr2()
            return RegexASTNode(RegexASTNode.CAT_EXPR, self.letter_class, left=left, right=right)
        
        return left

    def check_expr3(self):
        return self.check_expr4()

    def parse_expr3(self):
        subtree = self.parse_expr4()
        
        while self.check("*"):
            self.match("*")
            subtree = RegexASTNode(RegexASTNode.REP_EXPR, self.letter_class, left=subtree)

        return subtree

    def check_expr4(self):
        return self.check("0") or self.check("(") or self.letter_class.is_letter(self.head())

    def parse_expr4(self):
        if self.check("0"):
            return RegexASTNode(RegexASTNode.EPSILON, self.letter_class)
        elif self.letter_class.is_letter(self.head()):
            letter = self.letter_class.from_str(self.head())
            self.advance()
            return RegexASTNode(RegexASTNode.LETTER, self.letter_class, value=letter)
        else:
            self.match("(")
            expr = self.parse_expr()
            self.match(")")
            return expr
