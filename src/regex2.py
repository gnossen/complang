from letter import *
from letter_string import *
from regex_parser import *
from alphabet import *
from alphabet_union import *
from fsm import *
import random
import math
import numpy

class Regex:
    def __init__(self, letter_cls=None, letter_str=None, letter_list=None):
        if letter_cls is not None:
            if letter_str is None:
                raise Exception("Received letter_cls but no letter_str.")
            self._letter_cls = alphabet_union(letter_cls, RegexAlphabet)
            self._regex_str = LetterString(letter_cls=self._letter_cls, letter_str=letter_str)
        elif letter_list is not None:
            self._regex_str = LetterString(letter_list=letter_list)
            self._letter_cls = letter_list[0].__class__
        else:
            raise Exception("Must supply either letter_cls and letter_str or just letter_list.")

        parser = RegexParser(self._regex_str)
        self._ast = parser.parse()

    def __repr__(self):
        return str(self_regex_str)

    __str__ = __repr__
