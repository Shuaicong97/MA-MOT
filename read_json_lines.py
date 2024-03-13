import json

# 读取JSON文件
with open('meta_expressions/valid/meta_expressions.json', 'r') as file:
    data = json.load(file)

# 计算条目数量
videos_data = data.get('videos', {})

line_count = len(videos_data)

print(f'The number of entries in the JSON file is: {line_count}')


# 读取JSON文件
with open('meta_expressions/test/meta_expressions.json', 'r') as file:
    data = json.load(file)

# 计算条目数量
videos_data = data.get('videos', {})

line_count = len(videos_data)

print(f'The number of entries in the JSON file is: {line_count}')