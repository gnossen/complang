from letter import Letter

def alphabet(letters):
    def preprocess_letters():
        max_len = max([len(char) for char in letters])
        len_sorted_list = [[] for i in range(max_len)]

        for letter in letters:
            len_sorted_list[len(letter) - 1] += [letter]

        return len_sorted_list

    len_sorted_letters = preprocess_letters()

    class ListAlphabet(Letter):
        def __init__(self, str=None, id=None, letter=None):
            if letter is not None:
                if letter.__class__ is not self.__class__:
                    raise Exception("Cannot construct %s with %s." %
                                                    (self.__class__.__name__,
                                                    letter.__class__.__name__))
                self._id = letter.id()
            elif str is not None:
                if str not in letters:
                    raise Exception("'%s' is not a letter." % str)
                self._id = letters.index(str)
            elif id is not None:
                self._id = id
            else:
                raise Exception("ListAlphabet requires str, letter, or id argument.")

        def id(self):
            return self._id

        @staticmethod
        def size():
            return len(letters)

        def __repr__(self):
            return letters[self.id()]

        __str__ = __repr__

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
                    return (ListAlphabet(str=s), rem)

            raise Exception("'%s' is not a letter." % str)

        @classmethod
        def is_subalphabet(cls, other_alphabet):
            return other_alphabet is cls

    return ListAlphabet

