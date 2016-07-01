from fsm import *
from regex import *
from lang1 import *

regex = Regex(L1Letter)
regex.parse("A(AAB|AA*)")

fsm = FSM(L1Letter)
fsm.from_regex(regex.ast)
fsm.draw("regextest.png")
