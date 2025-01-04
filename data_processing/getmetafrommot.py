import csv
import json
import os
import re

length_dict_mot17 = {'MOT17-01': '00450', 'MOT17-02': '00600', 'MOT17-03': '01500', 'MOT17-04': '01050',
                     'MOT17-05': '00837', 'MOT17-06': '01194', 'MOT17-07': '00500', 'MOT17-08': '00625',
                     'MOT17-09': '00525', 'MOT17-10': '00654', 'MOT17-11': '00900', 'MOT17-12': '00900',
                     'MOT17-13': '00750', 'MOT17-14': '00750'}

length_dict_mot20 = {'MOT20-01': '00429', 'MOT20-02': '02782', 'MOT20-03': '02405', 'MOT20-05': '03315'}

'''
meta_expressions.json
    {
        "videos": {
            "<video_id>": {
                "expressions": {
                    "<expression_id>": {
                        "exp": "<expression>",
                        "obj": [
                            {
                                "obj_id": "<object_id>",
                                 "start_end_boundary": [
                                    {
                                        "start": "<start_frame>",
                                        "end": "<end_frame>"
                                    }
                                ]
                            }
                        ]
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


def clean_expressions(expressions):
    return {k: v for k, v in expressions.items() if v not in [[], {}]}


def add_frame_info(length_dict, video_name, frames):
    for key, value in length_dict.items():
        if key == video_name:
            for i in range(1, int(value) + 1):
                formatted_number = f"{i:05d}"
                frames.append(formatted_number)


# isTrain = false if it's for valid json.
def generate_yvos_meta_expressions(dataset, input_path, output_path, is_train):
    with open(input_path, 'r') as f:
        data = json.load(f)

    '''
    class 'dict': key must be unique 
    '''
    result = {'videos': {}}
    # Intermediate dictionary to collect frames based on query and track ID
    temp_dict = {}

    for entry in data:
        video_name = entry['Video']
        expression = entry['Language Query']
        if dataset == 'mot17':
            oid = entry['Track ID']
            start = entry['Start Frame']
            end = entry['End Frame']
        if dataset == 'mot20':
            oid = entry['IDs']
            start = entry['Start']
            end = entry['End']

        key = (video_name, expression, oid)

        if key not in temp_dict:
            temp_dict[key] = []

        temp_dict[key].append({
            'start_frame': start,
            'end_frame': end
        })

    for (video_name, expression, oid), appearances in temp_dict.items():
        if video_name not in result['videos']:
            result['videos'][video_name] = {'expressions': {}, 'frames': []}

        result['videos'][video_name]['expressions'] = clean_expressions(result['videos'][video_name]['expressions'])

        # Find the query ID for this expression
        # qid = len(result['videos'][video_name]['expressions']) + 1

        # Split oid into individual object IDs
        object_ids = oid.split(',')

        qid_found = None
        for qid, exp_data in result['videos'][video_name]['expressions'].items():
            if exp_data['exp'] == expression:
                qid_found = qid
                break

        if qid_found is None:
            qid_found = len(result['videos'][video_name]['expressions']) + 1
            result['videos'][video_name]['expressions'][qid_found] = {
                'exp': expression
            }
            if is_train:
                result['videos'][video_name]['expressions'][qid_found]['obj'] = []

        if is_train:
            for obj_id in object_ids:
                obj_id = obj_id.strip()

                obj_found = False
                for obj_entry in result['videos'][video_name]['expressions'][qid_found]['obj']:
                    if obj_entry['obj_id'] == obj_id:
                        obj_entry['start_end_boundary'].extend(appearances)
                        obj_found = True
                        break
                if not obj_found:
                    new_obj = {
                        'obj_id': obj_id,
                        'start_end_boundary': appearances
                    }
                    result['videos'][video_name]['expressions'][qid_found]['obj'].append(new_obj)
        else:
            found = False
            for existing_expression in result['videos'][video_name]['expressions'].values():
                if isinstance(existing_expression, dict) and existing_expression['exp'] == expression:
                    found = True
                    break

            if not found:
                result['videos'][video_name]['expressions'][qid_found] = {
                    'exp': expression
                }

    for video_name, video_data in result['videos'].items():
        video_data['expressions'] = clean_expressions(video_data['expressions'])

    # add frames information
    for entry in result['videos']:
        video_name = entry
        frames = result['videos'][video_name]['frames']
        if dataset == 'mot17':
            add_frame_info(length_dict_mot17, video_name, frames)
            # for key, value in length_dict_mot17.items():
            #     if key == video_name:
            #         for i in range(1, int(value)+1):
            #             formatted_number = f"{i:05d}"
            #             frames.append(formatted_number)
        if dataset == 'mot20':
            add_frame_info(length_dict_mot20, video_name, frames)

            # for key, value in length_dict_mot20.items():
            #     if key == video_name:
            #         for i in range(1, int(value)+1):
            #             formatted_number = f"{i:05d}"
            #             frames.append(formatted_number)

    print('result: ', result)
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)


mot17_training_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training-doubled-3.json'
meta_expressions_train = 'data/Ours/Rephrased/mot17/meta_expressions/train/meta_expressions.json'
mot17_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid-doubled-3.json'
meta_expressions_valid = 'data/Ours/Rephrased/mot17/meta_expressions/valid/meta_expressions.json'


def create_new_directory(filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory {directory} created.")
    else:
        print(f"Directory {directory} already exists.")

# directory = os.path.dirname(meta_expressions_valid)
# if not os.path.exists(directory):
#     os.makedirs(directory)
#     print(f"Directory {directory} created.")
# else:
#     print(f"Directory {directory} already exists.")


mot20_training_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training-doubled-3.json'
meta_expressions_train_mot20 = 'data/Ours/Rephrased/mot20/meta_expressions/train/meta_expressions.json'
mot20_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid-doubled-3.json'
meta_expressions_valid_mot20 = 'data/Ours/Rephrased/mot20/meta_expressions/valid/meta_expressions.json'

create_new_directory(meta_expressions_train)
create_new_directory(meta_expressions_valid)
create_new_directory(meta_expressions_train_mot20)
create_new_directory(meta_expressions_valid_mot20)


generate_yvos_meta_expressions('mot17', mot17_training_json, meta_expressions_train, True)
generate_yvos_meta_expressions('mot17', mot17_valid_json, meta_expressions_valid, False)
generate_yvos_meta_expressions('mot20', mot20_training_json, meta_expressions_train_mot20, True)
generate_yvos_meta_expressions('mot20', mot20_valid_json, meta_expressions_valid_mot20, False)


def generate_train_meta_json(dataset, input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)

    '''
    class 'dict': key must be unique 
    '''
    result = {'videos': {}}
    # store the value of 'videos', because <expression_id> is not unique.
    expressions_list = []

    for entry in data:
        video_name = entry['Video']
        if dataset == 'mot17':
            oid = entry['Track ID']  # = object_id. May occur "9,10" two IDs' situation.
        if dataset == 'mot20':
            oid = entry['IDs']

        if video_name not in result['videos']:
            result['videos'][video_name] = {'objects': {}}

        # Split oid into individual object IDs
        object_ids = oid.split(',')

        for obj_id in object_ids:
            if obj_id not in result['videos'][video_name]['objects']:
                result['videos'][video_name]['objects'][obj_id] = {'category': 'person', 'frames': []}
                # add frames information
                frames = result['videos'][video_name]['objects'][obj_id]['frames']
                if dataset == 'mot17':
                    add_frame_info(length_dict_mot17, video_name, frames)

                if dataset == 'mot20':
                    add_frame_info(length_dict_mot20, video_name, frames)

    print('meta result: ', type(result))
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)


meta_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Rephrased/mot17/train/meta.json'
meta_path_mot20 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Rephrased/mot20/train/meta.json'
create_new_directory(meta_path)
create_new_directory(meta_path_mot20)

generate_train_meta_json('mot17', mot17_training_json, meta_path)
generate_train_meta_json('mot20', mot20_training_json, meta_path_mot20)


def sort_meta(file_path, output_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    sorted_videos = dict(sorted(
        data['videos'].items(),
        key=lambda item: [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', item[0])]
    ))

    data['videos'] = sorted_videos

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)


sort_meta(meta_expressions_train, meta_expressions_train)
sort_meta(meta_expressions_valid, meta_expressions_valid)
sort_meta(meta_path, meta_path)
sort_meta(meta_expressions_train_mot20, meta_expressions_train_mot20)
sort_meta(meta_expressions_valid_mot20, meta_expressions_valid_mot20)
sort_meta(meta_path_mot20, meta_path_mot20)

print('process completed')
