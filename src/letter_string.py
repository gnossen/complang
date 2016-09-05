from letter import Letter

class LetterString:
    def __init__(self, letter_cls=None, str=None, letter_list=None):
        self._letter_cls = letter_cls
        if letter_list is not None:
            self._letter_list = letter_list
            if len(letter_list) == 0 and letter_cls is None:
                raise Exception("letter_list was empty and no letter_cls was supplied.")
            if len(letter_list) != 0:
                self._normalize_class([letter.__class__ for letter in letter_list])
        elif letter_cls is not None:
            if str is None:
                str = ""
            self._letter_list = self._letter_cls.parse(str)
        else:
            raise Exception("LetterString requires both letter_cls and str or just letter_list.")

    def _normalize_class(self, classes):
        new_letter_cls = LetterString._get_maximal_alphabet(classes)
        if new_letter_cls is not self._letter_cls:
            self._letter_cls = new_letter_cls
            self._letter_list = [self._letter_cls(letter=letter) for letter in self._letter_list]

    @staticmethod
    def _check_compatible_classes(cls1, cls2):
        if not cls1.is_subalphabet(cls2) and not cls2.is_subalphabet(cls1):
            raise Exception("Incompatible types.")

    @staticmethod
    def _get_maximal_alphabet(alphabets):
        for alphabet in alphabets:
            if all([alphabet.is_subalphabet(other_alphabet) for other_alphabet in alphabets]):
                return alphabet

        raise Exception("No maximal alphabet found.")

    def __repr__(self):
        return "".join([str(letter) for letter in self._letter_list])

    __str__ = __repr__

    def __eq__(self, other):
        if isinstance(other, str):
            return self.__eq__(LetterString(letter_cls=self._letter_cls, str=other))

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
        
        LetterString._check_compatible_classes(self._letter_cls, value.__class__)
        self._letter_list[key] = value

    def append(self, value):
        if isinstance(value, str):
            self.append(self._letter_cls(str=value))
            return

        LetterString._check_compatible_classes(self._letter_cls, value.__class__)
        self._letter_list.append(value)
        self._normalize_class([self._letter_cls, value.__class__])

    def __add__(self, other):
        if not isinstance(other, str) and \
                not isinstance(other, LetterString) and \
                not isinstance(other, Letter):
           raise Exception("Cannot concatenate type '%s' with LetterClass." % type(other))

        if isinstance(other, str):
            return self.__add__(LetterString(letter_cls=self._letter_cls, str=other))

        new_str = LetterString(letter_cls=self._letter_cls, letter_list=self._letter_list)

        if issubclass(other.__class__, Letter):
            new_str.append(other)
            return new_str

        LetterString._check_compatible_classes(self._letter_cls, other._letter_cls)
        new_str._letter_list = self._letter_list + other._letter_list
        new_str._normalize_class([self._letter_cls, other._letter_cls])
        return new_str

    def embed(self):
        return [letter.embed() for letter in self._letter_list]
