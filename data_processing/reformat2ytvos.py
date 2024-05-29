import json
import os


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
        else:
            result['videos'][video_name]['expressions'][existing_index] = {
                'exp': expression
            }

    # add frames information
    frame_length_path = ''
    if isTrain:
        frame_length_path = '../data/generated_by_code/ovis_json/train_frames_length.json'
    else:
        frame_length_path = '../data/generated_by_code/ovis_json/valid_frames_length.json'

    if not os.path.exists(frame_length_path):
        raise FileNotFoundError(f"The path {frame_length_path} does not exist.")

    with open(frame_length_path, 'r') as file:
        length_dict = json.load(file)
        print(f'length_dict: {length_dict}')

    for video_name in result['videos']:
        frames = result['videos'][video_name]['frames']

        if video_name in length_dict:
            value = length_dict[video_name]

            for i in range(1, int(value) + 1):
                formatted_number = f"{i:06d}"
                frames.append(formatted_number)

    print('result: ', result)
    with open(output_path, 'w') as json_file:
        json.dump(result, json_file, indent=4)


generate_yvos_meta_expressions('../data/generated_by_code/ovis_json/ovis_train.json',
                               '../data/generated_by_code/ovis_json/meta_expressions/train/meta_expressions.json', True)
generate_yvos_meta_expressions('../data/generated_by_code/ovis_json/ovis_valid.json',
                               '../data/generated_by_code/ovis_json/meta_expressions/valid/meta_expressions.json', False)

print('Process completed')
