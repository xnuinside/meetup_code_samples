import json
from os.path import getsize
from pympler.asizeof import asizeof
import orjson
import ujson
import platform
print(platform.machine())
print(platform.version())
print(platform.platform())

file_path = 'data/cargo.json'

print('File size', getsize(file_path), 'bytes')
print(f'File size {getsize(file_path)/1048576:.2f}', 'mbytes')


with open(file_path, 'r') as json_file:
	json_dict = json.load(json_file)

with open(file_path, 'r') as json_file:
	json_txt = json_file.read()

dict_python_from_json_str = eval(str(json_dict))

print("Txt massive", asizeof(json_txt), 'bytes')
print("Txt massive", asizeof(json_txt)/1048576, 'mbytes')

print("JSON module")
print(asizeof(json_dict), 'bytes')
print(f'{asizeof(json_dict)/1048576:.2f}', 'mbytes')

orjson_dict = orjson.loads(json_txt)
print("orjson package")
print(asizeof(orjson_dict), 'bytes')
print(f'{asizeof(orjson_dict)/1048576:.2f}', 'mbytes')

with open(file_path, 'r') as json_file:
	ujson_dict = ujson.load(json_file)

# also, funny fact: ujson does not support long ints https://github.com/esnme/ultrajson/issues/252
print("ujson package")
print(asizeof(ujson_dict), 'bytes')
print(f'{asizeof(ujson_dict)/1048576:.2f}', 'mbytes')

print("eval json string to pure Python")
print(asizeof(dict_python_from_json_str), 'bytes')
print(f'{asizeof(dict_python_from_json_str)/1048576:.2f}', 'mbytes')


global_1 = 1
global_2 = 1
global_1345_1 = 1345
global_1345_2 = 1345
global_str_1 = "python"
global_str_2 = "python"
global_long_string_1 = "python is a very funny language"
global_long_string_2 = "python is a very funny language"

with open("data/small_json.json", 'r') as small_json:
	small_json_dict = json.load(small_json)
	in_context_int = 1
	in_context_1345 = 1345
	in_context_str = "python"
	in_context_long_str = "python is a very funny language"

print("global vars")
print("1", id(global_2), id(global_1), id(in_context_int))
print("1345", id(global_1345_1), id(global_1345_2), id(in_context_1345))
print("python", id(global_str_1), id(global_str_2), id(in_context_str))
print("python is a very funny language", id(global_long_string_1), id(global_long_string_2), id(in_context_long_str))
print('dict1')
print('1', id(small_json_dict[0]['1']), id(small_json_dict[0]['11']))
print('1345', id(small_json_dict[0]['1345']), id(small_json_dict[0]['1345']))
print('python', id(small_json_dict[0]['2']), id(small_json_dict[0]['21']))
print('python is a very funny language', id(small_json_dict[0]['long_str']), id(small_json_dict[0]['long_str1']))
print('dict2')
print('1', id(small_json_dict[1]['1']), id(small_json_dict[1]['11']))
print('1345', id(small_json_dict[1]['1345']), id(small_json_dict[1]['1345']))
print('python', id(small_json_dict[1]['2']), id(small_json_dict[1]['21']))
print('python is a very funny language', id(small_json_dict[1]['long_str']), id(small_json_dict[1]['long_str1']))
print('dict3')
print('1', id(small_json_dict[2]['1']), id(small_json_dict[2]['11']))
print('1345', id(small_json_dict[2]['1345']), id(small_json_dict[2]['1345']))
print('python', id(small_json_dict[2]['2']), id(small_json_dict[2]['21']))
print('python is a very funny language', id(small_json_dict[2]['long_str']), id(small_json_dict[2]['long_str1']))
print('dict4')
print('1', id(small_json_dict[3]['1']), id(small_json_dict[3]['11']))
print('1345', id(small_json_dict[3]['1345']), id(small_json_dict[3]['1345']))
print('python', id(small_json_dict[3]['2']), id(small_json_dict[3]['21']))
print('python is a very funny language', id(small_json_dict[3]['long_str']), id(small_json_dict[3]['long_str1']))

# create one more context to check context vars
with open("data/small_json.json", 'r') as small_json:
	small_json_dict = json.load(small_json)
	sec_in_context_int = 1
	sec_in_context_1345 = 1345
	sec_in_context_str = "python"
	sec_in_context_long_str = "python is a very funny language"
