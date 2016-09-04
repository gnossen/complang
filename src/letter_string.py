from letter import Letter

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
        if not isinstance(key, int) and not isinstance(key, slice):
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
