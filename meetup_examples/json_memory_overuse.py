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

# ujson does not support long ints https://github.com/esnme/ultrajson/issues/252
print("ujson package")
print(asizeof(ujson_dict), 'bytes')
print(f'{asizeof(ujson_dict)/1048576:.2f}', 'mbytes')

print("eval json string to pure Python")
print(asizeof(dict_python_from_json_str), 'bytes')
print(f'{asizeof(dict_python_from_json_str)/1048576:.2f}', 'mbytes')