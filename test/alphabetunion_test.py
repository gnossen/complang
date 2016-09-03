from letter import *
from alphabetunion import *

def test_alphabetunion():
    L1 = alphabet_from_letters(["A", "B", "C"])
    L2 = alphabet_from_letters(["*", "(", ")", "|"])
    regex_alphabet = alphabet_union(L1, L2)
