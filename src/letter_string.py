from letter import Letter

def to_letter(obj, letter_cls):
    if isinstance(obj, str):
        return letter_cls(str=obj)

    if not issubclass(obj.__class__, Letter):
        raise Exception("%s is not an instance of Letter" % obj)

    if letter_cls is obj.__class__:
        return obj

    LetterString._check_compatible_classes(letter_cls, obj.__class__)
    return obj

def to_letter_string(obj, letter_cls):
    if isinstance(obj, str):
        return LetterString(letter_cls=letter_cls, str=obj)

    if issubclass(obj.__class__, Letter):
        return LetterString(letter_cls=letter_cls, letter_list=[to_letter(obj, letter_cls)])

    if not isinstance(obj, LetterString):
        raise Exception("'%s' not an instance of LetterString." % str(obj))

    LetterString._check_compatible_classes(letter_cls, obj._letter_cls)
    return obj

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
        try:
            other_ = to_letter_string(other, self._letter_cls)
        except:
            return False
        return all([this_letter == that_letter for (this_letter, that_letter) in zip(self._letter_list, other_._letter_list)])

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

        value_ = to_letter(value, self._letter_cls)
        LetterString._check_compatible_classes(self._letter_cls, value_.__class__)
        self._letter_list[key] = value_

    def append(self, value):
        value_ = to_letter(value, self._letter_cls)
        self._letter_list.append(value_)
        self._normalize_class([self._letter_cls, value_.__class__])

    def __add__(self, other):
        other_ = to_letter_string(other, self._letter_cls)
        new_str = LetterString(letter_cls=self._letter_cls, letter_list=self._letter_list)
        new_str._letter_list = self._letter_list + other_._letter_list
        new_str._normalize_class([self._letter_cls, other_._letter_cls])
        return new_str

    def __iter__(self):
        for letter in self._letter_list:
            yield letter

    def embed(self):
        return [letter.embed() for letter in self._letter_list]
