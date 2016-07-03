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
            if self.left.type == RegexASTNode.CAT_EXPR or self.left.type == RegexASTNode.OR_EXPR:
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
