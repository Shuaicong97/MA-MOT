import json
import os
import re


ovis_training_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training.json'
ovis_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid.json'
mot17_training_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.json'
mot17_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.json'
mot20_training_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training.json'
mot20_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid.json'

videos = [ovis_training_json, ovis_valid_json, mot17_training_json, mot17_valid_json, mot20_training_json, mot20_valid_json]


def get_videos(file_path):
    videos = set()
    with open(file_path, 'r') as file:
        data = json.load(file)

    for entry in data:
        video_name = entry['Video']
        videos.add(video_name)

    videos_list = list(videos)
    videos_list.sort()
    file_name_without_extension = os.path.splitext(file_path)[0]
    video_name_path = file_name_without_extension + '-videos-name.json'
    with open(video_name_path, 'w') as json_file:
        json.dump(videos_list, json_file)

    return videos_list


def get_all_videos():
    sum_videos = 0
    for video in videos:
        sum_videos += len(get_videos(video))
    print('Total number of videos: {}'.format(sum_videos))


print(f"All ovis videos ({len(get_videos(ovis_training_json))+len(get_videos(ovis_valid_json))}): {get_videos(ovis_training_json)}")
print(f"All ovis train, valid videos ({len(get_videos(ovis_training_json)), len(get_videos(ovis_valid_json))}): {get_videos(ovis_valid_json)}")
print(f"All mot17 videos ({len(get_videos(mot17_training_json))+len(get_videos(mot17_valid_json))}): {get_videos(mot17_training_json)}")
print(f"All mot17 train, valid videos ({len(get_videos(mot17_training_json)), len(get_videos(mot17_valid_json))}): {get_videos(mot17_valid_json)}")
print(f"All mot20 videos ({len(get_videos(mot20_training_json))+len(get_videos(mot20_valid_json))}): {get_videos(mot20_training_json)}")
print(f"All mot20 train, valid videos ({len(get_videos(mot20_training_json)), len(get_videos(mot20_valid_json))}): {get_videos(mot20_valid_json)}")
get_all_videos()
