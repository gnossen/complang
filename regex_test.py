from regex import *
from lang1 import *

regex = Regex(L1Letter)
print(L1Letter.is_letter("("))
regex.parse("AB*(A|B)")
print(regex.ast)
