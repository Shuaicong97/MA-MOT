# Second step: get number of frames of train and valid videos
import csv
import json
import pandas as pd
import os


def get_videos(file_path):
    videos = set()
    with open(file_path, 'r') as file:
        data = json.load(file)

    for entry in data:
        video_name = entry['Video']
        videos.add(video_name)

    return list(videos)


def get_frames_from_annotations(video_name):
    with open('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/annotations_train.json', 'r') as f:
        data = json.load(f)

    for entry in data['videos']:
        file_names = entry['file_names']
        if file_names:
            prefix = file_names[0].split('/')[0]
            if prefix == video_name:
                length = entry['length']
                # print(f"Video Name: {video_name}, Length: {length}")
                return length

    print(f"Video Name: {video_name} not found in annotations.")
    return None


train_json_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/ovis_train.json'
valid_json_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/ovis_valid.json'
train_list = get_videos(train_json_path)
valid_list = get_videos(valid_json_path)

print(f"Train videos: {len(train_list)}. Valid videos: {len(valid_list)}")

train_frames_dict = {}
valid_frames_dict = {}
not_found_in_train_dict = {}

def generate_video_frames_dict(video_list, video_type):
    for video_name in video_list:
        if get_frames_from_annotations(video_name) is not None:
            if video_type == 'train':
                train_frames_dict[video_name] = f"{get_frames_from_annotations(video_name):06d}"
            if video_type == 'valid':
                valid_frames_dict[video_name] = f"{get_frames_from_annotations(video_name):06d}"
        else:
            not_found_in_train_dict[video_type] = video_name


generate_video_frames_dict(train_list, 'train')
print(f'train_frames_dict ({len(train_frames_dict)}): {train_frames_dict}')
generate_video_frames_dict(valid_list, 'valid')
print(f'valid_frames_dict ({len(valid_frames_dict)}): {valid_frames_dict}')
print(f'not_found_in_train_dict ({len(not_found_in_train_dict)}): {not_found_in_train_dict}')

train_frames_json_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/train_frames_length.json'
valid_frames_json_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/valid_frames_length.json'


with open(train_frames_json_path, 'w') as json_file:
    json.dump(train_frames_dict, json_file, indent=4)
print(f"Data has been written to {train_frames_json_path}")

with open(valid_frames_json_path, 'w') as json_file:
    json.dump(valid_frames_dict, json_file, indent=4)
print(f"Data has been written to {valid_frames_json_path}")

with open(train_frames_json_path, 'r', encoding='utf-8') as file:
    meta_data = json.load(file)
    keys_count = len(meta_data.keys())
print(f"The number of keys in {train_frames_json_path}: {keys_count}")

with open(valid_frames_json_path, 'r', encoding='utf-8') as file:
    meta_data = json.load(file)
    keys_count = len(meta_data.keys())
print(f"The number of keys in {valid_frames_json_path}: {keys_count}")

