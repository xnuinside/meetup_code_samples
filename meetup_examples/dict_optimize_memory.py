from pympler.asizeof import asizeof
from dataclasses import dataclass
from collections import namedtuple
from frozendict import frozendict

cargo_example = {"id": 12318912,
                 "product": {"name": "Elec'sOil", "uid": "elec109ui"},
                 "quantity": {"value": 2380, "id": "mt"},
                 "dates": {"start": "2200-10-14T00:00:00", "end": "2200-11-11T00:00:00"}}

print("Size of dict", asizeof(cargo_example))
print("Size of dict 'product'", asizeof(cargo_example["product"]))
print("Size of dict 'quantity'", asizeof(cargo_example["quantity"]))
print("Size of dict 'dates'", asizeof(cargo_example["dates"]))


class Base:
    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]


class Product(Base):

    def __init__(self, name, uid):
        self.name = name
        self.uid = uid


class ProductSlots(Base):
    __slots__ = ['name', 'uid']

    def __init__(self, name, uid):
        self.name = name
        self.uid = uid


one_product = Product("Elec'sOil", "elec109ui")

print("Size of one Product", asizeof(one_product))
print("Size of one Product __dict__", asizeof(one_product.__dict__))

one_product_slots = ProductSlots("Elec'sOil", "elec109ui")
print("Size of one ProductSlots", asizeof(one_product_slots))

simple_tuple = ("Elec'sOil", "elec109ui")
# py3.7:  200
print("Size of one simple_tuple", asizeof(simple_tuple))

product = namedtuple("ProductNamedTuple", ['name', 'uid'])
pr_named_tuple = product("Elec'sOil", "elec109ui")
# py3.7:  200
print("Size of one named tuple", asizeof(pr_named_tuple))


frozendict_product = frozendict({"name": "Elec'sOil", "uid": "elec109ui"})
print("Size of one Frozen Dict", asizeof(frozendict_product))


@dataclass
class ProductNamedDataclass:
    name: str
    uid: str


dataclass_product = ProductNamedDataclass("Elec'sOil", "elec109ui")
# py3.7: 424
print("Size of dataclass", asizeof(dataclass_product))


class BaseSlots:

    __slots__ = []

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getitem__(self, key):
        return self.__getattribute__(key)


class ProductSlotsWithBaseSlots(BaseSlots):

    __slots__ = ['name', 'uid']

    def __init__(self, name, uid):
        self.name = name
        self.uid = uid


one_product_slots = ProductSlotsWithBaseSlots("Elec'sOil", "elec109ui")
print("Size of one ProductSlotsWithBaseSlots", asizeof(one_product_slots))

print(one_product_slots['name'])
one_product_slots['name'] = 'new'
print(one_product_slots['name'])


class OptimizedQuantity(BaseSlots):

    __slots__ = ['value', 'id']

    def __init__(self, value, id):
        self.value = value
        self.id = id


class Cargo(BaseSlots):

    __slots__ = ['id', 'dates', 'product', 'quantity']

    def __init__(self, id, dates, product, quantity):
        self.id = id
        self.dates = dates
        self.product = product
        self.quantity = quantity


class Dates(BaseSlots):

    __slots__ = ['start', 'end']

    def __init__(self, start, end):
        self.start = start
        self.end = end


cargo_optimised = Cargo("123123", Dates("2200-10-14T00:00:00", "2200-11-11T00:00:00"),
                        ProductSlotsWithBaseSlots("Elec'sOil", "elec109ui"),
                        OptimizedQuantity(450, "mt"))

# size of dict - 1816
print("cargo_dict_example:", asizeof(cargo_example))

# optimized structure - 512
print("cargo_optimised:", asizeof(cargo_optimised))
print(cargo_optimised['product']['name'])


# yes, but we have grapql schemas only

multi_cargo_example = [
                {"id": 12318912,
                 "product": {"name": "Elec'sOil", "uid": "elec109ui"},
                 "quantity": {"value": 2380, "id": "mt"},
                 "dates": {"start": "2200-10-14T00:00:00", "end": "2200-11-11T00:00:00"}},
                {"id": 22318912,
                 "product": {"name": "Elec'sOil", "uid": "elec109ui"},
                 "quantity": {"value": 380, "id": "mt"},
                 "dates": {"start": "2200-11-14T00:00:00", "end": "2200-12-11T00:00:00"}},
                {"id": 32318912,
                 "product": {"name": "Elec'sOil", "uid": "elec109ui"},
                 "quantity": {"value": 2000, "id": "mt"},
                 "dates": {"start": "2201-10-24T00:00:00", "end": "2230-11-11T00:00:00"}},
                {"id": 42318912,
                 "product": {"name": "Duper", "uid": "duper123"},
                 "quantity": {"value": 1500, "id": "mt"},
                 "dates": {"start": "2202-10-14T00:00:00", "end": "2203-11-11T00:00:00"}},
                {"id": 52318912,
                 "product": {"name": "Duper", "uid": "duper123"},
                 "quantity": {"value": 60000, "id": "mt"},
                 "dates": {"start": "2201-10-14T00:00:00", "end": "2201-11-11T00:00:00"}}]

class_mapper = {
    "id": lambda x: x,
    "dates": Dates,
    "product": ProductSlotsWithBaseSlots,
    "quantity": OptimizedQuantity
}

print('Size of multicargo list with dicts', asizeof(multi_cargo_example))

optimized_multi_cargo = []


def converter(dict_to_convert, _class_mapper):
    for key in dict_to_convert:
        if isinstance(multi_cargo_example[0][key], dict):
            yield {key: _class_mapper[key](**dict_to_convert[key])}
        else:
            yield {key: _class_mapper[key](dict_to_convert[key])}


for i in multi_cargo_example:
    kwargs = {}
    [kwargs.update(value) for value in converter(i, class_mapper)]
    optimized_multi_cargo.append(Cargo(**kwargs))

print('Size of multicargo list with objects', asizeof(optimized_multi_cargo))

# 1216 - py3.6
print(optimized_multi_cargo[0]['id'])
print(optimized_multi_cargo[2]['product']['name'])


class OptimisedBaseUniq:

    __slots__ = []

    _instances = {}

    def __new__(cls, *args, **kwargs):
        # you can make it better!
        instance_args = str(list(args) + list(kwargs.values()))
        if instance_args in cls._instances:
            return cls._instances[instance_args]
        else:
            obj = super(OptimisedBaseUniq, cls).__new__(cls)
            cls._instances[instance_args] = obj
            return obj

    def __getitem__(self, key):
        return self.__getattribute__(key)


class ProductUnique(OptimisedBaseUniq):

    __slots__ = ['name', 'uid']

    def __init__(self, name, uid):
        self.name = name
        self.uid = uid


one_product_slots = ProductUnique("Elec'sOil", uid="elec109ui")
print("Size of one ProductSlotsWithOptimisedBase", asizeof(one_product_slots))

optimized_multi_cargo_unique_product = []

class_mapper = {
    "id": lambda x: x,
    "dates": Dates,
    "product": ProductUnique,
    "quantity": OptimizedQuantity
}


for i in multi_cargo_example:
    kwargs = {}
    [kwargs.update(value) for value in converter(i, class_mapper)]
    optimized_multi_cargo_unique_product.append(Cargo(**kwargs))

print('Size of multicargo list with unique objects', asizeof(optimized_multi_cargo_unique_product))

# 4248
print('Size same data with unique per args class-dict-behavior',
      asizeof(optimized_multi_cargo_unique_product))

multi_cargo_example_frozen = []

for i in range(len(multi_cargo_example)):
    multi_cargo_example_frozen.append(frozendict(multi_cargo_example[i]))

print("Size of frozen dict", asizeof(multi_cargo_example_frozen))


multi_cargo_example = [{"id": "123123",
                        "dates": {"start": "2020-10-10", "end": "2020-11-10"}, "product": {"name":
                                                                                                          "Elec'sOil",
                                                                                "uid": "elec109ui",
                                                                    }, "quantity": {
                                                                        "value": 450,
                                                                        "id": "mt"
                                                                    }},
                       {"id": "223123", "dates": {"start": "2020-12-12", "end": "2021-01-10"}, "product": {"name":
                                                                                                               "Elec'sOil",
                                                                                "uid": "elec109ui",
                                                                    }, "quantity": {
                                                                        "value": 4500,
                                                                        "id": "mt"
                                                                    }},
                       {"id": "323123","dates": {"start": "2020-11-10", "end": "2020-12-10"}, "product": {"name":
                                                                                                              "Elec'sOil",
                                                                                           "uid": "elec109ui",
                                                                                           }, "quantity": {
                           "value": 1450,
                           "id": "mt"
                       }},
{"id": "423123","dates": {"start": "2020-11-10", "end": "2020-12-10"}, "product": {"name":
                                                                                                              "Elec'sOil",
                                                                                           "uid": "elec109ui",
                                                                                           }, "quantity": {
                           "value": 11450,
                           "id": "mt"
                       }},
{"id": "523123","dates": {"start": "2020-11-10", "end": "2020-12-10"}, "product": {"name":
                                                                                                              "Elec'sOil",
                                                                                           "uid": "elec109ui",
                                                                                           }, "quantity": {
                           "value": 2450,
                           "id": "mt"
                       }}
                       ]


products = {"elec109ui": {"name": "Elec'sOil", "uid": "elec109ui"}}


multi_cargo_example_with_unique_dict = [{"id": "123123",
                        "dates": {"start": "2020-10-10", "end": "2020-11-10"}, "product": products["elec109ui"],
                                         "quantity": {
                                                                        "value": 450,
                                                                        "id": "mt"
                                                                    }},
                       {"id": "223123", "dates": {"start": "2020-12-12", "end": "2021-01-10"}, "product": products["elec109ui"], "quantity": {
                                                                        "value": 4500,
                                                                        "id": "mt"
                                                                    }},
                       {"id": "323123","dates": {"start": "2020-11-10", "end": "2020-12-10"},  "product": products["elec109ui"], "quantity": {
                           "value": 1450,
                           "id": "mt"
                       }},
{"id": "423123","dates": {"start": "2020-11-10", "end": "2020-12-10"}, "product": products["elec109ui"], "quantity": {
                           "value": 11450,
                           "id": "mt"
                       }},
{"id": "523123","dates": {"start": "2020-11-10", "end": "2020-12-10"}, "product": products["elec109ui"], "quantity": {
                           "value": 2450,
                           "id": "mt"
                       }}
                       ]

# py 37: 6528
print("Size of base dict: ", asizeof(multi_cargo_example))
# py 37: 5536
print("Size of dict with unique product: ", asizeof(multi_cargo_example_with_unique_dict))

# same because of naive python optimization
print(id(multi_cargo_example_with_unique_dict[3]['quantity']['id']),
      id(multi_cargo_example_with_unique_dict[4]['quantity']['id']))


# check that type annotations does not inrease objects memory usage

class ProductUniqueWithTypeAnnotations(OptimisedBaseUniq):

    __slots__ = ['name', 'uid']

    def __init__(self, name: str, uid:str):
        self.name = name
        self.uid = uid


class ProductUniqueWithTypeAnnotationsCustomTyoes(OptimisedBaseUniq):

    __slots__ = ['name','uid']

    def __init__(self, name: OptimizedQuantity, uid:Dates):
        self.name = name
        self.uid = uid


one_product_slots = ProductUniqueWithTypeAnnotations("Elec'sOil", uid="elec109ui")
print("Size of one ProductUniqueWithTypeAnnotations", asizeof(one_product_slots))

one_product_slots = ProductUniqueWithTypeAnnotationsCustomTyoes("Elec'sOil", uid="elec109ui")
print("Size of one ProductUniqueWithTypeAnnotationsCustomTyoes", asizeof(one_product_slots))