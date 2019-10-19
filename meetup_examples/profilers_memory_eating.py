from guppy import hpy
a = lambda: 10
h = hpy()
# heap size: 4619038 bytes
print(h.heap())
# imports must be here to check heap size step by step
from memory_profiler import profile
# heap size: 7085995 bytes
print(h.heap())
# add decorator profiler to our test method
main = profile(a)
# heap size: 7091331
print(h.heap())

main()
# heap size: 7770723
print(h.heap())

# report from memory_profiler
# Line #    Mem usage    Increment   Line Contents
# ================================================
#     2     19.2 MiB     19.2 MiB   a = lambda: 10
