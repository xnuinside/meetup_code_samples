from copy import copy
from os.path import getsize
import timeit

from dict_optimize_memory import Cargo, converter, ProductSlotsWithBaseSlots, Dates, OptimizedQuantity, ProductUnique
from pympler.asizeof import asizeof
data_file = 'data/cargo.json'
print("\n########## Start performance testing ")
print(f"File size: {getsize(data_file)} bytes \n\t\t {getsize(data_file)/1048576:.4f} mbytes")
# load data to pure python dict
with open(data_file) as cargo_file:
    multi_cargo_example = eval(cargo_file.read())


optimized_multi_cargo_unique_product = []

# convert to optimised objects from dict_optimize_memory
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

print(f'Size with optimized unique product objects', asizeof(optimized_multi_cargo_unique_product),
      'bytes', f'{asizeof(optimized_multi_cargo_unique_product)/1048576:.4f}', 'mbytes')


optimized_multi_cargo_product = []

# convert to optimised objects from dict_optimize_memory
class_mapper = {
    "id": lambda x: x,
    "dates": Dates,
    "product": ProductSlotsWithBaseSlots,
    "quantity": OptimizedQuantity
}

for i in multi_cargo_example:
    kwargs = {}
    [kwargs.update(value) for value in converter(i, class_mapper)]
    optimized_multi_cargo_product.append(Cargo(**kwargs))

print(f'Size with optimized objects', asizeof(optimized_multi_cargo_product),
      'bytes', f'{asizeof(optimized_multi_cargo_product)/1048576:.4f}', 'mbytes')


def find_all_dates_in_multi_cargo_example():
    dates = [event['dates'] for event in multi_cargo_example]
    return dates


def find_all_dates_in_optimized():
    dates = [event['dates'] for event in optimized_multi_cargo_unique_product]
    return dates


def find_all_dates_in_optimized_access_by_arg():
    dates = [event.dates for event in optimized_multi_cargo_unique_product]
    return dates


print("\nFind all dates and return list")
print(timeit.timeit(find_all_dates_in_multi_cargo_example, number=1000))
print(timeit.timeit(find_all_dates_in_optimized, number=1000))
print(timeit.timeit(find_all_dates_in_optimized_access_by_arg, number=1000))


def find_product_with_name_dict():
    for i in multi_cargo_example:
        if i['product']['name'] == "Elec'sOil":
            return i


def find_product_with_name_in_optimized():
    for i in optimized_multi_cargo_unique_product:
        if i['product']['name'] == "Elec'sOil":
            return i


def find_first_product_byid_in_optimized():
    for i in optimized_multi_cargo_unique_product:
        if i.product.name == "Elec'sOil":
            return i


print('\nFind first product with name with for')
print('Dict ', timeit.timeit(find_product_with_name_dict, number=10000))
print('Objects by dict keys', timeit.timeit(find_product_with_name_in_optimized, number=10000))
print('Objects by id', timeit.timeit(find_first_product_byid_in_optimized, number=10000))


cargo_copy_dict = copy(multi_cargo_example)
cargo_copy_optimized = copy(optimized_multi_cargo_unique_product)


def while_products_all_dates_in_multi_cargo_example():
    while cargo_copy_dict:
        i = cargo_copy_dict.pop()
        if i['product']['name'] == "Elec'sOil":
            return i


def while_all_dates_in_optimized():
    while cargo_copy_optimized:
        i = cargo_copy_optimized.pop()
        if i['product']['name'] == "Elec'sOil":
            return i


def while_all_dates_in_optimized_with_arg():
    while cargo_copy_optimized:
        i = cargo_copy_optimized.pop()
        if i.product.name == "Elec'sOil":
            return i


print("\nSearch first elem with product name == Elec'sOil with while and pop")
print('Dict ',timeit.timeit(while_products_all_dates_in_multi_cargo_example, number=10000))
print('Objects by dict keys', timeit.timeit(while_all_dates_in_optimized, number=10000))
print('Objects by id', timeit.timeit(while_all_dates_in_optimized_with_arg, number=10000))


def get_id_in_multi_cargo_example():
    for i in multi_cargo_example:
        return i['id']


def get_id_in_optimized():
    for i in optimized_multi_cargo_unique_product:
        return i['id']


def get_id_by_arg_optimized():
    for i in optimized_multi_cargo_unique_product:
        return i.id


print("\nReturn id of first element")
print('Dict ', timeit.timeit(get_id_in_multi_cargo_example, number=10000))
print('Objects by dict keys', timeit.timeit(get_id_in_optimized, number=10000))
print('Objects by id', timeit.timeit(get_id_by_arg_optimized, number=10000))

print(f'Dicts size       ', asizeof(multi_cargo_example),'bytes', f'{asizeof(multi_cargo_example)/1048576:.4f}',
      'mbytes')

print(f'Size with optimized objects', asizeof(optimized_multi_cargo_unique_product),
      'bytes',
      f'{asizeof(optimized_multi_cargo_unique_product)/1048576:.4f}', 'mbytes')


def find_product_with_name_dict_list():
    return [i for i in multi_cargo_example if i['product']['name'] == "Elec'sOil"]


def find_first_product_byid_in_optimized_list():
    return [i for i in optimized_multi_cargo_unique_product if i.product.name == "Elec'sOil"]


print('\nFind all elems with product == name with for and return list')
print('Dict ', timeit.timeit(find_product_with_name_dict_list, number=10000))
print('Objects by dict keys', timeit.timeit(find_first_product_byid_in_optimized_list, number=10000))


def find_product_with_name_dict_list_and_extract_attr():
    return [i['id'] for i in multi_cargo_example if i['product']['name'] == "Elec'sOil"]


def find_first_product_byid_in_optimized_list_and_extract_attr():
    return [i.id for i in optimized_multi_cargo_unique_product if i.product.name == "Elec'sOil"]


print('\nFind all elems with product == name with for and return list')
print('Dict ', timeit.timeit(find_product_with_name_dict_list_and_extract_attr, number=10000))
print('Objects by dict keys', timeit.timeit(find_first_product_byid_in_optimized_list_and_extract_attr, number=10000))


