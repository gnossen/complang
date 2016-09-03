from letter import *
from letter_string import *
from alphabet import *
from regexast import *
from fsm import *
import random
import math
import numpy

regex_alphabet = alphabet(["(", ")", "*", "|"])

class Regex:
    def __init__(self, letter_cls=None, letter_str=None, letter_list=None):
        self._regex_str = LetterString(letter_cls=letter_cls, letter_str=letter_str, letter_list=letter_list)
        self._parse()


