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


csv_to_json('./Grounded Tracking Annotations - MOT17(Ashiq).csv', './gta_ashiq_all.json')
csv_to_json('./Grounded Tracking Annotations - MOT17(Seenat).csv', './gta_seenat_all.json')


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

with open('gta_ashiq_all.json', 'r') as f:
    data = json.load(f)

'''
class 'dict': key must be unique 
'''
result = {'videos': {}}
# store the value of 'videos', because <expression_id> is not unique.
expressions_list = []

for entry in data:
    video_name = entry['Video']
    qid = entry['QID']
    expression = entry['Language Query']
    oid = entry['IDs']  # = object_id
    start = entry['Start']
    end = entry['End']

    if video_name not in result['videos']:
        result['videos'][video_name] = {'expressions': {}, 'frames': []}

    if qid not in result['videos'][video_name]['expressions']:
        result['videos'][video_name]['expressions'][qid] = []

    result['videos'][video_name]['expressions'][qid].append({
        'exp': expression,
        'obj_id': oid
    })


# add frames information
for entry in result['videos']:
    print('entry:', entry)
    video_name = entry
    frames = result['videos'][video_name]['frames']
    print('frames:', frames)
    for key, value in length_dict.items():
        if key == video_name:
            print(value)
            for i in range(1, int(value)+1):
                formatted_number = f"{i:06d}"
                frames.append(formatted_number)
    print('after frames:', frames)


print('result: ', result)

with open('gta_ashiq_yvos.json', 'w') as json_file:
    json.dump(result, json_file, indent=2)

print('process completed')
