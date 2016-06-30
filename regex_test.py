from regex import *
from lang1 import *

regex = Regex(L1Letter)
regex.parse("AB*(A|B)")
print(regex.ast)

for i in range(10):
    str = regex.generate()
    print(str)
    print([letter.embed() for letter in str])

print("")
print(regex.embed())

print("")
for i in range(10):
    r = Regex(L1Letter)
    r.generate_regex()
    print(r.ast)
