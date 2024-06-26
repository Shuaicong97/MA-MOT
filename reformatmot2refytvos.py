import csv
import json


def csv_to_json(csv_file_path, json_file_path):
    csv_data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    with open(json_file_path, 'w') as json_file:
        json.dump(csv_data, json_file, indent=2)


# csv_to_json('Grounded Tracking Annotations - MOT17(Ashiq).csv', 'gta_ashiq_all.json')
# csv_to_json('Grounded Tracking Annotations - MOT17(Seenat).csv', 'gta_seenat_all.json')

# csv_to_json('Grounded Tracking Annotations - MOT17 - 5 Train.csv', 'gta_train_all.json')
# csv_to_json('Grounded Tracking Annotations - MOT17 - 2 Valid.csv', 'gta_valid_all.json')


length_dict = {'MOT17-02': '00600', 'MOT17-04': '01050', 'MOT17-05': '00837',
               'MOT17-09': '00525', 'MOT17-10': '00654', 'MOT17-11': '00900',
               'MOT17-13': '00750'}

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


# isTrain = false if it's for valid json.
def generate_yvos_meta_expressions(input_path, output_path, isTrain):

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
        oid = entry['Track ID']  # = object_id
        start = entry['Start Frame']
        end = entry['End Frame']

        if video_name not in result['videos']:
            result['videos'][video_name] = {'expressions': {}, 'frames': []}

        if qid not in result['videos'][video_name]['expressions']:
            result['videos'][video_name]['expressions'][qid] = []

        # Split oid into individual object IDs
        object_ids = oid.split(',')

        if isTrain:
            for obj_id in object_ids:
                result['videos'][video_name]['expressions'][qid].append({
                    'exp': expression,
                    'obj_id': obj_id.strip()
                })
        else:
            result['videos'][video_name]['expressions'][qid] = {
                'exp': expression
            }

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


generate_yvos_meta_expressions('gta_train_all.json', 'data/mot17/meta_expressions/train/meta_expressions.json', True)
generate_yvos_meta_expressions('gta_valid_all.json',
                               'data/mot17/meta_expressions/valid/meta_expressions.json', False)


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

    print('result: ', result)
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=2)


generate_train_meta_json('gta_train_all.json', 'data/mot17/train/meta.json')


def calculate_expression_sum(video_data):
    expression_sum = 0
    for video_id, video_info in video_data.items():
        for expression_id, expression_info in video_info.get('expressions', {}).items():
            expression_sum += 1
    #         print(video_id, expression_info)
    # print(expression_sum)
    return expression_sum


with open('data/Ref-YT/meta_expressions/valid/meta_expressions.json', 'r') as f:
    data = json.load(f)

videos = data.get('videos', {})
count = 0
expression_sum = 0
for video_id, video_info in videos.items():
    count += 1
    expression_sum += calculate_expression_sum({video_id: video_info})
    if count % 25 == 0 or count == len(videos):
        print(f"For videos {count-24} to {count}, expression sum is: {expression_sum}")
        expression_sum = 0


print('process completed')
