from regex import *
from lang1 import *

# regex = Regex(L1Letter)
# regex.parse("AB*(A|B)")
# print(regex.ast)
# 
# for i in range(10):
#     str = regex.generate()
#     print(str)
#     embedding = [letter.embed() for letter in str]
#     print(embedding)
# 
# print("")
# for i in range(10):
#     r = Regex(L1Letter)
#     r.generate_regex()
#     print(r)
# 
#     embedding = r.embed()
#     print(embedding)
#     r_prime = Regex(L1Letter)
#     r_prime.from_embedding(embedding)
# 
#     print(r_prime)

regex = Regex(L1Letter)
regex.parse("B*A(B|C)(B|AAB)(BBAB)*")
print(regex)
