from letter import *

def alphabet_union(cls_A, cls_B):
    class UnionLetter(Letter):
        def __init__(self, letter):
            self.letter = letter
            if letter.__class_ is cls_A:
                self._id = letter.id()
            elif letter.__class__ is cls_B:
                self._id = letter.id() + cls_A.size()
            else:
                raise Exception("Yo, what's going on up there?")

        @staticmethod
        def size(self):
            return cls_A.size() + cls_B.size()

        @staticmethod
        def from_str(str):
            if cls_A.is_letter(str):
                return UnionLetter(cls_A.from_str(str))
            elif cls_B.is_letter(str):
                return UnionLetter(cls_B.from_str())
            else:
                raise Exception("You think we take just anything down here?")

        @staticmethod
        def is_letter(str):
            return cls_A.is_letter(str) or cls_B.is_letter(str)

        def __repr__(self):
            return self.letter.__repr__()

        __str__ = __repr__

        def id(self):
            return self._id
        
    return UnionLetter
