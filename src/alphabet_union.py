from letter import *

def alphabet_union(cls_A, cls_B):
    cls_A_letters = set([str(letter) for letter in cls_A.all()])
    cls_B_letters = set([str(letter) for letter in cls_B.all()])
    common_letters = cls_A_letters & cls_B_letters
    if len(common_letters) != 0:
        raise Exception("Cannot take union with common letters: %s" % str(common_letters))

    class UnionLetter(Letter):
        def __init__(self, id=None, str=None, letter=None):
            if letter is not None:
                if cls_A.is_subalphabet(letter.__class__):
                    cls_A_letter = cls_A(letter=letter)
                    self._id = cls_A_letter.id()
                elif cls_B.is_subalphabet(letter.__class__):
                    cls_B_letter = cls_B(letter=letter)
                    self._id = cls_A.size() + cls_B_letter.id()
                else:
                    raise Exception("Received letter not a member of %s or %s." %
                                                (cls_A.__name__,
                                                 cls_B.__name__))
            elif str is not None:
                if cls_A.is_letter(str):
                    cls_A_letter = cls_A(str=str)
                    self.__init__(letter=cls_A_letter)
                elif cls_B.is_letter(str):
                    cls_B_letter = cls_B(str=str)
                    self.__init__(letter=cls_B_letter)
                else:
                    raise Exception("Received letter not a member of %s or %s." %
                                                (cls_A.__name__,
                                                 cls_B.__name__))
            elif id is not None:
                self._id = id
            else:
                raise Exception("UnionAlphabet requires str, letter, or id arguments.")

        def _get_class(self):
            if self.id() < cls_A.size():
                return cls_A
            return cls_B

        def _get_subalphabet_letter(self):
            cls = self._get_class()
            sub_id = self.id()
            if cls is cls_B:
                sub_id -= cls_A.size()
            return cls(id=sub_id)

        @staticmethod
        def size():
            return cls_A.size() + cls_B.size()

        @staticmethod
        def is_letter(str):
            return cls_A.is_letter(str) or cls_B.is_letter(str)

        def __repr__(self):
            return self._get_subalphabet_letter().__repr__()

        __str__ = __repr__

        def id(self):
            return self._id

        @staticmethod
        def parse_one(str):
            letter_A = None
            rem_A = None
            try:
                letter_A, rem_A = cls_A.parse_one(str)
            except:
                pass

            letter_B = None
            rem_B = None
            try:
                letter_B, rem_B = cls_B.parse_one(str)
            except:
                pass
            
            if letter_A is not None and letter_B is not None:
                if rem_A < rem_B:
                    return (letter_A, rem_A)
                else:
                    return (letter_B, rem_B)
            elif letter_A is not None:
                return (letter_A, rem_A)
            elif letter_B is not None:
                return (letter_B, rem_B)
            else:
                raise Exception("Cannot parse %s as either %s or %s" %
                                        (str, cls_A.__name__, cls_B.__name__))
            

        @classmethod
        def is_subalphabet(cls, other_alphabet):
            return cls_A.is_subalphabet(other_alphabet) or cls_B.is_subalphabet(other_alphabet)
        
    return UnionLetter
