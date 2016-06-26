import abc

# Note: 
#   Much consideration was put into this name
#   This concept can be used to generalize both phonemes and graphemes
#   the term articuleme could be used to convey the fact that a member of this class
#   is a single atomic element of the ariculatory space, but the term "letter" actually
#   exists

class Letter:
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
