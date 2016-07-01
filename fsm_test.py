from fsm import *
from regex import *
from lang1 import *

regex = Regex(L1Letter)
regex.parse("A(AAB|AA*)")

fsm = FSM(L1Letter)
fsm.from_regex(regex.ast)
fsm.draw("regextest.png")

regex2 = Regex(L1Letter)
regex2.parse("ABBA")

fsm2 = FSM(L1Letter)
fsm2.from_regex(regex2.ast)
fsm2.draw("regextest2.png")


regex3 = Regex(L1Letter)
regex3.parse("A(A|B)*B")

fsm3 = FSM(L1Letter)
fsm3.from_regex(regex3.ast)
fsm3.draw("regextest3.png")
