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


length_dict = {'MOT17-02': '000600', 'MOT17-04': '001050', 'MOT17-05': '000837',
               'MOT17-09': '000525', 'MOT17-10': '000654', 'MOT17-11': '000900',
               'MOT17-13': '000750'}

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


def generate_yvos_meta_expressions(input_path, output_path):
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

        for obj_id in object_ids:
            result['videos'][video_name]['expressions'][qid].append({
                'exp': expression,
                'obj_id': obj_id.strip()
            })

    # add frames information
    for entry in result['videos']:
        video_name = entry
        frames = result['videos'][video_name]['frames']
        for key, value in length_dict.items():
            if key == video_name:
                print(value)
                for i in range(1, int(value)+1):
                    formatted_number = f"{i:06d}"
                    frames.append(formatted_number)

    print('result: ', result)
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=2)


# generate_yvos_meta_expressions('gta_train_all.json', 'data/meta_expressions/train/meta_expressions.json')
# generate_yvos_meta_expressions('gta_valid_all.json', 'data/meta_expressions/valid/meta_expressions.json')


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
                            formatted_number = f"{i:06d}"
                            frames.append(formatted_number)

    print('result: ', result)
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=2)


generate_train_meta_json('gta_train_all.json', 'data/train/mock_category/meta.json')

print('process completed')
