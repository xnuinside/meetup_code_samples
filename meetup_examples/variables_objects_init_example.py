import dis
from pympler.asizeof import asizeof
import sys

low_int_str ="Low integers behavior test"
start = "############### Start ################"
end = "############### End ################"

print(f"{low_int_str}\n{start}")
# ints from -5 to 256 always have same id
a = 12
b = 12
c = 12
d = 12
f = 12
g = 12

print(id(a), id(b), id(c), id(d), id(f), id(g))


def function_1_with_low_ints(call_number):

    print(f"Function 1 call number {call_number}")
    a = 12
    b = 12
    c = 12
    d = 12
    f = 12
    g = 12

    print(id(a), id(b), id(c), id(d), id(f), id(g))
function_1_with_low_ints(1)
function_1_with_low_ints(2)


def function_2_with_low_ints(call_number):
    print(f"Function 2 call number {call_number}")
    a = 12
    b = 12
    c = 12
    d = 12
    f = 12
    g = 12

    print(id(a), id(b), id(c), id(d), id(f), id(g))


function_2_with_low_ints(1)
function_2_with_low_ints(2)
print(f"{low_int_str}\n{end}")
# this sample about initialisation of integer not in -5 to 256 range
# I saw in one article sample from REPL and a conclusion, that for integers not in -5 to 256
# each time created new object - but this is not true

a = 257
b = 257
c = 257
d = 257
f = 257
g = 257

# True
print(a is g)
# True
print(f is c)
# True
print(b is d)
# all ids the same, because all variables contain link to one object
print(id(a), id(b), id(c), id(d), id(f), id(g))



a = (1,2,)
b = (1,2,)
d = (1,2,)
c = (1,2,)
# same id in 3.7, different ids in 3.6
print(id(a), id(b),  id(d), id(c))

# mathematical operations
a = 2
b = 3
c = 5
d = 5
f = a + b

# all ids same, because low integers in -5 to 256
print(id(f), id(c), id(d))

# mathematical operations
a = 200
b = 300
c = 500
d = 500
f = 200 + 300

# in 3.6 f will be different from c and d, in 3.7 - will be the same all 3 ids
print(id(f), id(c), id(d))

# mathematical operations
a = 200
b = 300
c = 500
d = 500
# pay attention to this line
f = a + b

# in 3.6 and in 3.7!! f will be different from c and d, interning does not  working
print(id(f), id(c), id(d))


# defaults initialisation, why you should not use mutable objects in functions defaults
def cat_relative_ids(cat_id, cat_family=[]):
    [cat_family.append(x) for x in range(10)]
    return cat_family

cat_relative_ids(1)
ids = cat_relative_ids(2)
# will be 20, because cat_family one object for all functions calls
print(len(ids))

dis.dis(cat_relative_ids)


def cat_relative_ids_no_defaults(cat_id, cat_family):
    [cat_family.append(x) for x in range(10)]
    return cat_family


print('function memory before call', asizeof(cat_relative_ids))
print('function memory before call no defaults', asizeof(cat_relative_ids_no_defaults))

cat_relative_ids(1, [])
cat_relative_ids_no_defaults(1, [])
# pympler asizeof does not work correct with function objects
print('function memory after call', asizeof(cat_relative_ids))
print('function memory after call no defaults', asizeof(cat_relative_ids_no_defaults))
print('function __defaults__', asizeof(cat_relative_ids))

"""
Intern'' the given string.  This enters the string in the (global)
table of interned strings whose purpose is to speed up dictionary lookups.
Return the string itself or the previously interned string object with the
same value.
"""
