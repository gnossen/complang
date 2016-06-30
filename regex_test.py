from regex import *
from lang1 import *

regex = Regex(L1Letter)
regex.parse("AB*(A|B)")
print(regex.ast)

for i in range(10):
    print(regex.generate())

print("")
print(regex.embed())
