import csv
import json
import os
import re

def csv_to_json(csv_file_path, json_file_path):
    csv_data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    with open(json_file_path, 'w') as json_file:
        json.dump(csv_data, json_file, indent=2)


length_dict = {'MOT17-01': '00450', 'MOT17-02': '00600', 'MOT17-03': '01500', 'MOT17-04': '01050',
               'MOT17-05': '00837', 'MOT17-06': '01194', 'MOT17-07': '00500', 'MOT17-08': '00625',
               'MOT17-09': '00525', 'MOT17-10': '00654', 'MOT17-11': '00900', 'MOT17-12': '00900',
               'MOT17-13': '00750', 'MOT17-14': '00750'}

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


# isTrain = false if it's for valid json.
def generate_yvos_meta_expressions(input_path, output_path, isTrain):

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
        oid = entry['Track ID']
        start = entry['Start Frame']
        end = entry['End Frame']

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
            if isTrain:
                result['videos'][video_name]['expressions'][qid_found]['obj'] = []

        if isTrain:
            # if qid_found is None:
            #     qid_found = len(result['videos'][video_name]['expressions']) + 1
            #     result['videos'][video_name]['expressions'][qid_found] = {
            #         'exp': expression,
            #         'obj': []
            #     }

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
                # if isinstance(existing_expression, list):
                #     for exp in existing_expression:
                #         if exp['exp'] == expression:
                #             found = True
                #             break
                # elif isinstance(existing_expression, dict):
                #     if existing_expression['exp'] == expression:
                #         found = True
                #         break
                # if found:
                #     break
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
        for key, value in length_dict.items():
            if key == video_name:
                print(value)
                for i in range(1, int(value)+1):
                    formatted_number = f"{i:05d}"
                    frames.append(formatted_number)

    print('result: ', result)
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)


mot17_training_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.json'
meta_expressions_train = 'data/Ours/mot17/meta_expressions/train/meta_expressions.json'
mot17_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.json'
meta_expressions_valid = 'data/Ours/mot17/meta_expressions/valid/meta_expressions.json'

directory = os.path.dirname(meta_expressions_train)
if not os.path.exists(directory):
    os.makedirs(directory)
    print(f"Directory {directory} created.")
else:
    print(f"Directory {directory} already exists.")

directory = os.path.dirname(meta_expressions_valid)
if not os.path.exists(directory):
    os.makedirs(directory)
    print(f"Directory {directory} created.")
else:
    print(f"Directory {directory} already exists.")

generate_yvos_meta_expressions(mot17_training_json, meta_expressions_train, True)
generate_yvos_meta_expressions(mot17_valid_json, meta_expressions_valid, False)


def generate_train_meta_json(input_path, output_path):
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
        qid = entry['Query ID']
        expression = entry['Language Query']
        oid = entry['Track ID']  # = object_id. May occur "9,10" two IDs' situation.
        start = entry['Start Frame']
        end = entry['End Frame']

        if video_name not in result['videos']:
            result['videos'][video_name] = {'objects': {}}

        # Split oid into individual object IDs
        object_ids = oid.split(',')

        for obj_id in object_ids:
            if obj_id not in result['videos'][video_name]['objects']:
                result['videos'][video_name]['objects'][obj_id] = {'category': 'person', 'frames': []}
                # add frames information
                frames = result['videos'][video_name]['objects'][obj_id]['frames']
                for key, value in length_dict.items():
                    if key == video_name:
                        print(value)
                        for i in range(1, int(value) + 1):
                            formatted_number = f"{i:05d}"
                            frames.append(formatted_number)

    print('meta result: ', type(result))
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)


meta_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/mot17/train/meta.json'
directory = os.path.dirname(meta_path)
if not os.path.exists(directory):
    os.makedirs(directory)
    print(f"Directory {directory} created.")
else:
    print(f"Directory {directory} already exists.")

generate_train_meta_json(mot17_training_json, meta_path)


def calculate_expression_sum(video_data):
    expression_sum = 0
    for video_id, video_info in video_data.items():
        for expression_id, expression_info in video_info.get('expressions', {}).items():
            expression_sum += 1
    #         print(video_id, expression_info)
    # print(expression_sum)
    return expression_sum


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


print('process completed')
