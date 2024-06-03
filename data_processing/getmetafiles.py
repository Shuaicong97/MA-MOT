# Third step: get JPEGImages and generate meta_expressions and meta files
import json
import os
import shutil

video_ids_map = {}

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

    for entry in data:
        video_name = entry['Video']
        expression = entry['Language Query']
        oid = entry['IDs']  # = object_id
        start = entry['Start']
        end = entry['End']

        if video_name not in result['videos']:
            result['videos'][video_name] = {'expressions': {}, 'frames': []}
            expression_index = 1

        existing_index = None
        for index, expr in result['videos'][video_name]['expressions'].items():
            if isTrain and expr[0]['exp'] == expression:
                existing_index = index
                break
            if not isTrain and expr['exp'] == expression:
                existing_index = index
                break

        if existing_index is None:
            existing_index = str(expression_index)
            result['videos'][video_name]['expressions'][existing_index] = []
            expression_index += 1

        # Split oid into individual object IDs
        object_ids = oid.split(',')

        if isTrain:
            for obj_id in object_ids:
                result['videos'][video_name]['expressions'][existing_index].append({
                    'exp': expression,
                    'obj_id': obj_id.strip()
                })
            if video_name not in video_ids_map:
                video_ids_map[video_name] = set()
            video_ids_map[video_name].add(oid)
        else:
            result['videos'][video_name]['expressions'][existing_index] = {
                'exp': expression
            }

    # add frames information
    frame_length_path = ''
    if isTrain:
        frame_length_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/train_frames_length.json'
    else:
        frame_length_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/valid_frames_length.json'

    if not os.path.exists(frame_length_path):
        raise FileNotFoundError(f"The path {frame_length_path} does not exist.")

    with open(frame_length_path, 'r') as file:
        length_dict = json.load(file)
        # print(f'length_dict: {length_dict}')

    for video_name in result['videos']:
        frames = result['videos'][video_name]['frames']

        if video_name in length_dict:
            value = length_dict[video_name]

            for i in range(1, int(value) + 1):
                formatted_number = f"{i:05d}"
                frames.append(formatted_number)

    # print(f'result ({isTrain}): {result}')
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)


ovis_train_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/ovis_train.json'
ovis_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/ovis_valid.json'
meta_train_file = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/ovis/meta_expressions/train/meta_expressions.json'
meta_valid_file = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/ovis/meta_expressions/valid/meta_expressions.json'

generate_yvos_meta_expressions(ovis_train_json, meta_train_file, True)
generate_yvos_meta_expressions(ovis_valid_json, meta_valid_file, False)


def sort_json_by_obj_id(file_path, output_file):
    with open(file_path, 'r') as file:
        data = json.load(file)

    for video_id, video_data in data['videos'].items():
        for expression_id, expression_list in video_data['expressions'].items():
            sorted_list = sorted(expression_list, key=lambda x: int(x['obj_id']))
            video_data['expressions'][expression_id] = sorted_list

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Sorted data has been saved to {output_file}")


# sort_json_by_obj_id(meta_train_file, meta_train_file)

ovis_train_videos = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/train'
train_jpeg = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/ovis/train/JPEGImages'
valid_jpeg = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/ovis/valid/JPEGImages'

with open(meta_train_file, 'r', encoding='utf-8') as file:
    meta_data = json.load(file)
train_video_ids = meta_data['videos'].keys()  # 373 videos
# print(len(train_video_ids))

with open(meta_valid_file, 'r', encoding='utf-8') as file:
    meta_data = json.load(file)
valid_video_ids = meta_data['videos'].keys()  # 160 videos
# print(len(valid_video_ids))

for video_name in video_ids_map:
    video_ids_map[video_name] = sorted(video_ids_map[video_name], key=int)
print(f'video_ids_map: {video_ids_map}')

if not os.path.exists(train_jpeg):
    os.makedirs(train_jpeg)
if not os.path.exists(valid_jpeg):
    os.makedirs(valid_jpeg)


def copy_videos_to_target(target_folder, video_type):
    if video_type == 'train':
        video_ids = train_video_ids
    if video_type == 'valid':
        video_ids = valid_video_ids
    i = 0
    for subdir in os.listdir(ovis_train_videos):
        subdir_path = os.path.join(ovis_train_videos, subdir)
        if os.path.isdir(subdir_path) and subdir in video_ids:
            target_path = os.path.join(target_folder, subdir)
            if os.path.exists(target_path):
                shutil.rmtree(target_path)
            shutil.copytree(subdir_path, target_path)
            i = i + 1
    print(f'number of videos: {i}')


copy_videos_to_target(train_jpeg, 'train')
copy_videos_to_target(valid_jpeg, 'valid')

annotations_train = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/annotations_train.json'


def generate_train_meta_json(input_path, output_path):
    with open(annotations_train, 'r') as f:
        anno = json.load(f)
    id_name_dict = {}
    for category in anno['categories']:
        id_name_dict[category["id"]] = category["name"]
    print(f'id_name_dict: {id_name_dict}')

    with open(input_path, 'r') as f:
        data = json.load(f)

    result = {'videos': {}}
    # store the value of 'videos', because <expression_id> is not unique.
    expressions_list = []
    for entry in data:
        video_name = entry['Video']
        qid = entry['QID']
        expression = entry['Language Query']
        oid = entry['IDs']
        start = entry['Start']
        end = entry['End']

        if video_name not in result['videos']:
            result['videos'][video_name] = {'objects': {}}

        # Split oid into individual object IDs
        object_ids = oid.split(',')

        for obj_id in object_ids:
            if obj_id not in result['videos'][video_name]['objects']:
                category = ''
                for key, value in id_name_dict.items():
                    if str(key) == obj_id:
                        category = value
                        break
                result['videos'][video_name]['objects'][obj_id] = {'category': category, 'frames': []}

                # add frames information
                frames = result['videos'][video_name]['objects'][obj_id]['frames']
                frame_length_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/train_frames_length.json'
                with open(frame_length_path, 'r') as file:
                    length_dict = json.load(file)

                if video_name in length_dict:
                    value = length_dict[video_name]
                    for i in range(1, int(value) + 1):
                        formatted_number = f"{i:05d}"
                        frames.append(formatted_number)

    print('result: ', result)
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)


train_meta_file = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/ovis/train/meta.json'
# generate_train_meta_json(ovis_train_json, train_meta_file)


frame_length_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/train_frames_length.json'
output_directory = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/ovis/train/GTs'


def generate_gt_file():
    with open(frame_length_path, 'r') as file:
        length_dict = json.load(file)

    with open(annotations_train, 'r') as f:
        data = json.load(f)

    for key in length_dict:
        folder_path = os.path.join(output_directory, key)
        os.makedirs(folder_path, exist_ok=True)
        print(f'Created folder: {folder_path}')

        for video in data['videos']:
            video_id = video['id']
            file_name = video['file_names'][0].split('/')[0]
            if key == file_name:
                file_path = os.path.join(folder_path, f'gt.txt')
                with open(file_path, 'w') as f:
                    object_id_counter = 0

                    for annotation in data['annotations']:
                        frame_id_counter = 1  # start frame ID from 1
                        if annotation['video_id'] == video_id:
                            object_id_counter += 1
                            for bbox in annotation['bboxes']:
                                if bbox is not None:
                                    x, y, w, h = bbox
                                    # last three parameters (1, 1, 1) are fake default
                                    gt_line = f'{frame_id_counter}, {object_id_counter}, {x}, {y}, {w}, {h}, 1, 1, 1\n'
                                    print(f'{frame_id_counter}, {object_id_counter}, {x}, {y}, {w}, {h}, 1, 1, 1')
                                    f.write(gt_line)

                                frame_id_counter += 1

    print("conversion to gt.txt complete.")


# generate_gt_file()

print('Process completed')
