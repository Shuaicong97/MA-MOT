import json

# 读取JSON文件
with open('HC-STVG/anno_v2/query_v2.json', 'r') as file:
    data_dict = json.load(file)

line_count = len(data_dict.values())

print(f'The number of values in the JSON file is: {line_count}')