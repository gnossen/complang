from letter import *

class L1Letter(Letter):
    alphabet_size = 3

    @staticmethod
    def size():
        return L1Letter.alphabet_size

    def __repr__(self):
        A = ord('A')
        return str(chr(A + self._id))

    __str__ = __repr__

    @staticmethod
    def from_str(str):
        if len(str) != 1:
            raise Exception("Letters must have length 1.")
        
        return L1Letter(ord(str) - ord('A'))

    @staticmethod
    def is_letter(str):
        if str is None or len(str) != 1:
            return False

        id = L1Letter.from_str(str)._id
        return id < L1Letter.alphabet_size and id >= 0
