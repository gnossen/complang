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

def alphabet_from_letters(letters):
    def preprocess_letters():
        max_len = max([len(char) for char in letters])
        len_sorted_list = [[] for i in range(max_len)]

        for letter in letters:
            len_sorted_list[len(letter) - 1] += [letter]

        return len_sorted_list

    len_sorted_letters = preprocess_letters()

    class ListAlphabet(Letter):
        def __init__(self, str=None, id=None):
            if str is not None:
                if str not in letters:
                    raise Exception("'%s' is not a letter." % str)
                self._id = letters.index(str)
            elif id is not None:
                self._id = id
            else:
                raise Exception("ListAlphabet requires either str or id argument.")

        def id(self):
            return self._id

        @staticmethod
        def size():
            return len(letters)

        def __repr__(self):
            return letters[self.id()]

        __str__ = __repr__

        @staticmethod
        def from_str(str):
            try:
                return ListAlphabet(id=letters.index(str))
            except:
                raise Exception("Invalid letter '%s'." % str)

        @staticmethod
        def is_letter(str):
            return str in letters

        @staticmethod
        def parse_one(str):
            for i, letter_len_i in reversed(list(enumerate(len_sorted_letters))):
                i = i + 1
                if i > len(str):
                    continue

                s = str[:i]
                rem = str[i:]
                if s in letter_len_i:
                    return (ListAlphabet.from_str(s), rem)

            raise Exception("'%s' is not a letter." % str)

    return ListAlphabet

class LetterString:
    def __init__(self, letter_cls=None, str=None, letter_list=None):
        self._letter_cls = letter_cls
        if letter_list is not None and len(letter_list) != 0:
            self._letter_cls = letter_list[0].__class__
            if any([l for l in letter_list if l.__class__ is not self._letter_cls]):
                raise Exception("Received letter_list with heterogenous letter types: %s" % letter_list)
            self._letter_list = letter_list
        elif str is not None:
            self._letter_list = self._letter_cls.parse(str)
        else:
            raise Exception("LetterString requires both letter_cls and str or just letter_list.")

    def __repr__(self):
        return "".join([str(letter) for letter in self._letter_list])

    __str__ = __repr__

    def __eq__(self, other):
        return all([this_letter == that_letter for (this_letter, that_letter) in zip(self._letter_list, other._letter_list)])

    def __ne__(self, other):
        return not (self == other)

    def __len__(self):
        return len(self._letter_list)

    def __getitem__(self, key):
        if not isinstance(key, int):
            raise Exception("Index to LetterString must be int.")

        return self._letter_list[key] 

    def __setitem__(self, key, value):
        if not isinstance(key, int):
            raise Exception("Index to LetterString must be int.")

        if isinstance(value, str):
            self.__setitem__(key, self._letter_cls(str=value))
            return
        
        if value.__class__ != self._letter_cls:
            raise Exception("Attempted to set value of alphabet '%s' within LetterString of alphabet '%s'." % (value.__class__.__name__, self._letter_cls.__name__))

        self._letter_list[key] = value
