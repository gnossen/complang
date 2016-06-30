from regex import *
from lang1 import *

regex = Regex(L1Letter)
sample = "(BA|A*)*"
print(sample)
regex.parse(sample)
# regex.parse("C|C*B")
print(regex.ast)

regex = Regex(L1Letter)
regex.parse("AB*(A|B)")
print(regex.ast)

print("\nGenerating strings from regex:")
for i in range(10):
    s = regex.generate()
    print("".join([str(char) for char in s]))

print("\nGenerating random regexes.")
for i in range(10):
    r = Regex(L1Letter)
    r.generate_regex()
    print(r)

    embedding = r.embed()
    r_prime = Regex(L1Letter)
    r_prime.from_embedding(embedding)

    print(r_prime)
    print()
