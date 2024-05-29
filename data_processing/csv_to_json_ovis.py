import csv
import json
import pandas as pd


def read_csv_without_blank_columns(file_path, output_file_path):
    df = pd.read_csv(file_path)
    # remove all columns where the name is blank
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    int_columns = ['QID', 'IDs', 'Start', 'End']
    for column in int_columns:
        if column in df.columns:
            df[column] = df[column].astype(pd.Int64Dtype())
    df.to_csv(output_file_path, index=False)


def csv_to_json(csv_file_path, json_file_path):
    csv_data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    with open(json_file_path, 'w') as json_file:
        json.dump(csv_data, json_file, indent=2)


ashiq_csv = 'data/OVIS/Grounded Tracking Annotations - OVIS(Ashiq).csv'
# read_csv_without_blank_columns(ashiq_csv, ashiq_csv)

# seenat = valid, ashiq = train
# csv_to_json('data/OVIS/Grounded Tracking Annotations - OVIS(Seenat).csv',
#             'data/generated_by_code/ovis_json/ovis_seenat_all.json')
# csv_to_json('data/OVIS/Grounded Tracking Annotations - OVIS(Ashiq).csv',
#             'data/generated_by_code/ovis_json/ovis_ashiq_all.json')


def get_videos(file_path):
    videos = set()
    with open(file_path, 'r') as file:
        data = json.load(file)

    for entry in data:
        video_name = entry['Video']
        videos.add(video_name)

    return list(videos)


# print(f"All ashiq videos ({len(get_videos('data/generated_by_code/ovis_json/ovis_ashiq_all.json'))}): {get_videos('data/generated_by_code/ovis_json/ovis_ashiq_all.json')}")
# print(f"All seenat videos ({len(get_videos('data/generated_by_code/ovis_json/ovis_seenat_all.json'))}): {get_videos('data/generated_by_code/ovis_json/ovis_seenat_all.json')}")


'''
meta_expressions.json
    {
        "videos": {
            "<video_id>": {
                "expressions": {
                    "<expression_id>": {
                        "exp": "<expression>",
                        "obj_id": "<object_id>"
                    }
                },
                "frames": [
                    "<frame_id>",
                    "<frame_id>"
                    ]
                }
            }
        }
    }
'''


def get_frames_from_annotations(video_name):
    with open('../data/OVIS/annotations_train.json', 'r') as f:
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

train_json_path = '../data/generated_by_code/ovis_json/ovis_train.json'
valid_json_path = '../data/generated_by_code/ovis_json/ovis_valid.json'

train_list = get_videos(train_json_path)
valid_list = get_videos(valid_json_path)

print(f"All valid videos ({len(train_list)}): {len(valid_list)}")

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

train_frames_json_path = '../data/generated_by_code/ovis_json/train_frames_length.json'
valid_frames_json_path = '../data/generated_by_code/ovis_json/valid_frames_length.json'

with open(train_frames_json_path, 'w') as json_file:
    json.dump(train_frames_dict, json_file, indent=4)
print(f"Data has been written to {train_frames_json_path}")

with open(valid_frames_json_path, 'w') as json_file:
    json.dump(valid_frames_dict, json_file, indent=4)
print(f"Data has been written to {valid_frames_json_path}")






# def generate_train_meta_json(input_path, output_path):
#     with open(input_path, 'r') as f:
#         data = json.load(f)
#
#     '''
#     class 'dict': key must be unique
#     '''
#     result = {'videos': {}}
#     # store the value of 'videos', because <expression_id> is not unique.
#     expressions_list = []
#
#     for entry in data:
#         video_name = entry['Video']
#         qid = entry['Query ID']
#         expression = entry['Language Query']
#         oid = entry['Track ID']  # = object_id. May occur "9,10" two IDs' situation.
#         start = entry['Start Frame']
#         end = entry['End Frame']
#
#         if video_name not in result['videos']:
#             result['videos'][video_name] = {'objects': {}}
#
#         # Split oid into individual object IDs
#         object_ids = oid.split(',')
#
#         for obj_id in object_ids:
#             if obj_id not in result['videos'][video_name]['objects']:
#                 result['videos'][video_name]['objects'][obj_id] = {'category': 'person', 'frames': []}
#                 # add frames information
#                 frames = result['videos'][video_name]['objects'][obj_id]['frames']
#                 for key, value in length_dict.items():
#                     if key == video_name:
#                         print(value)
#                         for i in range(1, int(value) + 1):
#                             formatted_number = f"{i:06d}"
#                             frames.append(formatted_number)
#
#     print('result: ', result)
#     with open(output_path, 'w') as json_file:
#         json.dump(result, json_file, indent=2)


# generate_train_meta_json('gta_train_all.json', 'data/train/mock_category/meta.json')

def calculate_expression_sum(video_data):
    expression_sum = 0
    for video_id, video_info in video_data.items():
        for expression_id, expression_info in video_info.get('expressions', {}).items():
            expression_sum += 1
    #         print(video_id, expression_info)
    # print(expression_sum)
    return expression_sum


# with open('data/Ref-YT/meta_expressions/valid/meta_expressions.json', 'r') as f:
#     data = json.load(f)
#
# videos = data.get('videos', {})
# count = 0
# expression_sum = 0
# for video_id, video_info in videos.items():
#     count += 1
#     expression_sum += calculate_expression_sum({video_id: video_info})
#     if count % 25 == 0 or count == len(videos):
#         print(f"For videos {count-24} to {count}, expression sum is: {expression_sum}")
#         expression_sum = 0


print('process completed')
