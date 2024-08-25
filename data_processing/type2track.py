import pandas as pd
from io import StringIO
import json
import os

file_path1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Type-to-Track/annotations/v1.0/mot17_train_coco.json'
file_path2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Type-to-Track/annotations/v1.0/mot17_test_coco.json'
file_path3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Type-to-Track/annotations/v1.0/tao_train_coco.json'


def count_unique_pairs(json_data, total_number):
    unique_pairs = set()  # store the unique (track_id, caption) pair
    pairs_list = []  # store all (track_id, caption) pairs

    for annotation in json_data['annotations']:
        track_id = annotation['track_id']
        captions = annotation['captions']

        for caption in captions:
            if caption is not None:
                pair = (track_id, caption)
                if pair not in unique_pairs:
                    unique_pairs.add(pair)
                pairs_list.append(pair)

    # for pair in unique_pairs:
    #     print(f"Track ID: {pair[0]}, Caption: '{pair[1]}'")

    total_number += len(unique_pairs)
    print(f"Unique pairs: {len(unique_pairs)}")
    return total_number


# json_data = {
#     "annotations": [
#         {"id": 1, "track_id": 2, "captions": ["man in orange sweater and black pants", "man walking on sidewalk"]},
#         {"id": 2, "track_id": 1, "captions": ["man in orange sweater and black ", "man walking on sidewalk"]}
#     ]
# }

with open(file_path1, 'r') as f:
    json_data = json.load(f)
total_number = count_unique_pairs(json_data, 0)

with open(file_path2, 'r') as f:
    json_data = json.load(f)
total_number = count_unique_pairs(json_data, total_number)

with open(file_path3, 'r') as f:
    json_data = json.load(f)
total_number = count_unique_pairs(json_data, total_number)
print(total_number)


