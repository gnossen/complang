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

    @classmethod
    def parse(letter_class, str):
        if len(str) == 0:
            return []

        def parse_one(prefix, suffix):
            if letter_class.is_letter(prefix):
                return (prefix, suffix)

            if len(suffix) == 0:
                raise Exception("Could not parse %s as %s." % (prefix, letter_class.__name__))

            return parse_one(prefix + suffix[0], suffix[1:])

        letter, remainder = parse_one("", str)
        return [letter_class.from_str(letter)] + letter_class.parse(remainder)

    @classmethod
    def to_str(letter_class, letter_list):
        s = ""
        for letter in letter_list:
            s += str(letter)

        return s

