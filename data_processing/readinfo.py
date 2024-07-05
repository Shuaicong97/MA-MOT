import json

annotations_train = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/annotations_train.json'

with open(annotations_train, 'r') as file:
    data = json.load(file)

categories = [(item["id"], item["name"]) for item in data["categories"]]

categories_dict = {item["name"]: item["id"] - 1 for item in data["categories"]}

# name_dict = {item["name"] for item in data["categories"]}

name_dict = {item["name"]: item["id"] for item in data["categories"]}

# 按照 categories 中的 id 对 name_dict 进行排序
sorted_name_dict = dict(sorted(name_dict.items(), key=lambda x: x[1]))

print(sorted_name_dict)

