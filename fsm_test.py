from fsm import *
from regex import *
from lang1 import *

regex = Regex(L1Letter)
regex.parse("A(AAB|AA*)")

fsm = NFSM(L1Letter)
fsm.from_regex(regex.ast)
fsm.draw("regextest.png")

regex2 = Regex(L1Letter)
regex2.parse("ABBA")

fsm2 = NFSM(L1Letter)
fsm2.from_regex(regex2.ast)
fsm2.draw("regextest2.png")

regex3 = Regex(L1Letter)
regex3.parse("A(A|B)*B")

fsm3 = NFSM(L1Letter)
fsm3.from_regex(regex3.ast)
fsm3.draw("regextest3.png")

fsm4 = DFSM(L1Letter)
fsm4.from_nfsm(fsm3)
fsm4.draw("regextest4.png")

regex4 = Regex(L1Letter)
regex4.parse("A(AB|B)*B")
fsm5 = regex4.generate_fsm()
fsm5.draw("regextest5.png")
