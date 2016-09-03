import abc

# Note: 
#   Much consideration was put into this name
#   This concept can be used to generalize both phonemes and graphemes
#   the term articuleme could be used to convey the fact that a member of this class
#   is a single atomic element of the ariculatory space, but the term "letter" actually
#   exists

class Letter(object):
    @abc.abstractmethod
    def size(self): # pragma: no cover
        pass

    @abc.abstractmethod
    def __repr__(self): # pragma: no cover
        pass

    @abc.abstractmethod
    def from_str(str): # pragma: no cover
        pass

    @abc.abstractmethod
    def is_letter(str): # pragma: no cover
        pass

    @abc.abstractmethod
    def id(self): # pragma: no cover
        pass

    # want a concept of subalphabets that works with equality
    def __eq__(self, other):
        return self.__class__ == other.__class__  and self.id() == other.id()

    def __ne__(self, other):
        return not (self == other)


    @classmethod
    def all(letter_class):
        class LetterIterator:
            def __init__(self):
                self.i = 0

            def __iter__(self):
                return self

            def __next__(self):
                if self.i < letter_class.size():
                    ret_letter = letter_class(id=self.i)
                    self.i += 1
                    return ret_letter
                else:
                    raise StopIteration()

            next = __next__

        return LetterIterator()

    def embed(self):
        head = [0.0] * self.id()
        middle = [1.0]
        tail = [0.0] * (self.size() - self.id() - 1)
        return head + middle + tail

    # expected to return (letter, remain_str)
    @classmethod
    def parse_one(letter_cls, str): # pragma: no cover
        raise Exception("Abstract class method!")

    # deprecated
    @classmethod
    def parse(letter_class, str): # pragma: no cover
        if len(str) == 0:
            return []

        letter, remainder = letter_class.parse_one(str)
        return [letter] + letter_class.parse(remainder)

