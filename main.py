import json
import os
import torch

with open('annotations_train.json', 'r') as f:
    data = json.load(f)

target_folder = './gt'


def generate_mot_file():
    for video in data['videos']:
        video_id = video['id']
        file_name = video['file_names'][0].split('/')[0]
        # print(f'filename: {file_name}')
        file_path = os.path.join(target_folder, f'gt_{file_name}.txt')

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
                            mot_line = f'{frame_id_counter}, {object_id_counter}, {x}, {y}, {w}, {h}, 1, 1, 1\n'
                            print(f'{frame_id_counter}, {object_id_counter}, {x}, {y}, {w}, {h}, 1, 1, 1')
                            f.write(mot_line)

                        frame_id_counter += 1

    print("conversion to gt.txt complete.")


def calculate_move():
    numbers1 = [-1377, -1489, -1201, -928, -1297, -925, -1360, -1116, -1220, -1113, -1284,
               -1438, -1533, -1585, -1414, -1412, -1603]

    numbers2 = [-1428, -957, -1134, -993, -1079, -1239, -1078, -1220, -1171, -1363, -1438]
    numbers3 = [-1533, -1585, -1414, -1412, -1603, -1428, -1377, -994, -1347, -1172, -1241]
    numbers = [-1073, -1253, -1006, -1367, -1363, -1438, -1533, -1585, -1414, -1412, -1603]
    numbers = [-1377, -994, -1347, -1172, -1241, -1073, -1253, -1006, -1489]
    # result = [numbers[0] + 1550] + [num + 1560 for num in numbers[1:]]
    result = [num + 1560 for num in numbers]

    for num in result:
        print(num)


def read_pth_file():
    ctvis_vitl_ovis = torch.load('data/DVIS/weights/ctvis_vitl_ovis.pth', map_location=torch.device('cpu'))
    print(f'ctvis_vitl_ovis.pth: {ctvis_vitl_ovis.keys()}')
    offline_vitl_ovis_534 = torch.load('data/DVIS/weights/offline_vitl_ovis_534.pth', map_location=torch.device('cpu'))


def print_keys(d, depth=0):
    for key, value in d.items():
        print("  " * depth + str(key))
        if isinstance(value, dict):
            print_keys(value, depth + 1)


ctvis_vitl_ovis = torch.load('data/DVIS/weights/dinov2_vitl14_pretrain_.pth', map_location=torch.device('cpu'))
instances_predictions = torch.load('data/DVIS/output_DVIS_Plus_Offline_VitAdapterL_OVIS/inference/instances_predictions.pth', map_location=torch.device('cpu'))


def print_json_keys(data, indent=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print("  " * indent + str(key))
            if isinstance(value, (dict, list)):
                print_json_keys(value, indent + 1)
    elif isinstance(data, list):
        for item in data:
            print_json_keys(item, indent + 1)


def read_json_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


file_path = 'data/DVIS/output_DVIS_Plus_Offline_VitAdapterL_OVIS/inference/results.json'
json_data = read_json_file(file_path)


if __name__ == '__main__':
    # generate_mot_file()
    # calculate_move()
    # read_pth_file()
    print(instances_predictions)
    # print_json_keys(json_data)


