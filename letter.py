import abc

# Note: 
#   Much consideration was put into this name
#   This concept can be used to generalize both phonemes and graphemes
#   the term articuleme could be used to convey the fact that a member of this class
#   is a single atomic element of the ariculatory space, but the term "letter" actually
#   exists

class Letter(object):
    def __init__(self, _id):
        self._id = _id

    # The particular articulatory space should return the number of possible atomic elements
    @abc.abstractmethod
    def size(self):
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass

    @abc.abstractmethod
    def from_str(str):
        pass

    @abc.abstractmethod
    def is_letter(str):
        pass

    def id(self):
        return self._id

    @classmethod
    def all(letter_class):
        class LetterIterator:
            def __init__(self):
                self.i = 0

            def __iter__(self):
                return self

            def __next__(self):
                if self.i < letter_class.size():
                    ret_letter = letter_class(self.i)
                    self.i += 1
                    return ret_letter
                else:
                    raise StopIteration()

            next = __next__

        return LetterIterator()

    def embed(self):
        head = [0.0] * self._id
        middle = [1.0]
        tail = [0.0] * (self.size() - self._id - 1)
        return head + middle + tail
