from guppy import hpy

h = hpy()
# heap size: 4619038 bytes
print(h.heap())


from pympler.asizeof import asizeof


def funct_to_profile():
    a = lambda: 10
    b = lambda: 10
    print(h.heap())
    a()
    b()
    big_list_check = [{'1': 1} for _ in range(100000)]
    print("asizeof ", asizeof(big_list_check))
    print(h.heap())
    c = big_list_check

# imports must be here to check heap size step by step
from memory_profiler import profile
# heap size: 7085995 bytes
print(h.heap())
# add decorator profiler to our test method
main = profile(funct_to_profile)
# heap size: 7091331 bytes

main()
# great result
