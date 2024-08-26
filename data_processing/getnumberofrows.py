# number of rows as number of queries
import pandas as pd
from io import StringIO
import json
import os

sum_length = 0
# mot17_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.csv'  # 773
# mot17_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.csv'  # 698
# mot20_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training.csv'  # 2275
# mot20_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid.csv'  # 1670
# ovis_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training.csv'  # 3685
# ovis_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid.csv'  # 678

mot17_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training-doubled.json'  # 773 -> 1539
mot17_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid-doubled.json'  # 698 -> 1396
mot20_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training-doubled.json'  # 2275 -> 4545
mot20_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid-doubled.json'  # 1670 -> 3340
ovis_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training-doubled.json'  # 3685 -> 7370
ovis_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid-doubled.json'  # 678 -> 1356

# 19546

datasets = [mot17_training, mot17_valid, mot20_training, mot20_valid, ovis_training, ovis_valid]


# def count_rows_in_csv(file_path):
#     try:
#         df = pd.read_csv(file_path)
#         return len(df)
#     except Exception as e:
#         print(e)
#         return None
#
#
# row_counts = {}
# for file_path in datasets:
#     row_count = count_rows_in_csv(file_path)
#     sum_length += row_count
#     if row_count is not None:
#         row_counts[file_path] = row_count
#
# for file_path, row_count in row_counts.items():
#     print(f"{file_path}: {row_count} rows")
#
# print(sum_length)  # 9779


def count_objects_in_json(json_file):
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 检查JSON文件是否是数组类型
    if isinstance(data, list):
        # 返回数组中对象的数量
        return len(data)
    else:
        # 如果JSON不是数组，返回0或抛出错误
        return 0


# 使用示例
for file_path in datasets:
    object_count = count_objects_in_json(file_path)
    sum_length += object_count
    print(f'The number of objects in the JSON file is: {object_count}')

print(f'The number of total length is: {sum_length}')  # 19546


def print_json_hierarchy(data, indent=0, file=None):
    if isinstance(data, dict):
        for key, value in data.items():
            if file:
                file.write(' ' * indent + str(key) + '\n')
            else:
                print(' ' * indent + str(key))
            print_json_hierarchy(value, indent + 4, file)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if file:
                file.write(' ' * indent + f'[{i}]' + '\n')
            else:
                print(' ' * indent + f'[{i}]')
            print_json_hierarchy(item, indent + 4, file)
    else:
        if file:
            file.write(' ' * indent + str(data) + '\n')
        else:
            print(' ' * indent + str(data))


file_path1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Type-to-Track/annotations/v1.0/mot17_train_coco.json'
file_path2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Type-to-Track/annotations/v1.0/mot17_test_coco.json'
file_path3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Type-to-Track/annotations/v1.0/tao_train_coco.json'


def load_json_file(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return None
    if os.path.getsize(file_path) == 0:
        print(f"Error: File '{file_path}' is empty.")
        return None
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON from file '{file_path}'.")
        print(f"Details: {e}")
        return None


output_file_path1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Type-to-Track/hierachy_mot17_train_coco.txt'
output_file_path2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Type-to-Track/hierachy_mot17_test_coco.txt'
output_file_path3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Type-to-Track/hierachy_tao_train_coco.txt'


# def write_json_file(file_path, output_file_path):
#     json_data = load_json_file(file_path)
#     if json_data:
#         with open(output_file_path, 'w') as output_file:
#             print_json_hierarchy(json_data, file=output_file)


# write_json_file(file_path1, output_file_path1)
# write_json_file(file_path2, output_file_path2)
# write_json_file(file_path3, output_file_path3)

caption_count = 0


# def get_data(filepath):
#     with open(filepath, 'r') as file:
#         data = json.load(file)
#     return data
#
#
# file1 = get_data(file_path1)
# for annotation in file1['annotations']:
#     if 'captions' in annotation:
#         caption_count += len(annotation['captions'])
#         print(annotation['captions'])
#
# print(f'Total captions count: {caption_count}')
