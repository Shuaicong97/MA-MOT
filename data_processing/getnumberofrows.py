# number of rows as number of queries/tracks
import pandas as pd
from io import StringIO
import json
import os

mot17_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.json'  # 773
mot17_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.json'  # 698
mot20_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training.json'  # 2275
mot20_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid.json'  # 1670
ovis_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training.json'  # 3685
ovis_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid.json'  # 678
# #Tracks=9779

mot17_training_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/MOT17-training-doubled.json'
mot17_valid_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/MOT17-valid-doubled.json'
mot20_training_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/MOT20-training-doubled.json'
mot20_valid_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/MOT20-valid-doubled.json'
ovis_training_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/OVIS-training-doubled.json'
ovis_valid_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/OVIS-valid-doubled.json'
# #Queries=9779

datasets = [mot17_training, mot17_valid, mot20_training, mot20_valid, ovis_training, ovis_valid]
datasets_rephrased = [mot17_training_rephrased, mot17_valid_rephrased, mot20_training_rephrased, mot20_valid_rephrased, ovis_training_rephrased, ovis_valid_rephrased]


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


sum_length = 0
for file_path in datasets:
    object_count = count_objects_in_json(file_path)
    sum_length += object_count
    print(f'The number of objects in the JSON file is: {object_count}')

print(f'The number of tracks is: {sum_length}')  # 9779

sum_length = 0
for file_path in datasets_rephrased:
    object_count = count_objects_in_json(file_path)
    sum_length += object_count
    print(f'The number of objects in the JSON file is: {object_count}')

print(f'The number of queries is: {sum_length}')  # 19563