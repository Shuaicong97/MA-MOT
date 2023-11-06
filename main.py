import json

with open('annotations_train.json', 'r') as f:
    data = json.load(f)


def generate_mot_file():
    tmp_id = -1
    for video in data['videos']:
        video_id = video['id']
        file_name = video['file_names'][0].split('/')[0]
        # print(f'filename: {file_name}')

        with open(f'gt_{video_id}.txt', 'w') as f:
            object_id_counter = 0

            for annotation in data['annotations']:
                frame_id_counter = 1  # start frame ID from 1
                ann_id = annotation['id']

                if annotation['video_id'] == video_id:


                    if ann_id != tmp_id:
                        tmp_id = ann_id
                        object_id_counter += 1

                        for bbox in annotation['bboxes']:
                            if bbox is not None:
                                x, y, w, h = bbox
                                # last three parameters (1, 1, 1) are fake default
                                mot_line = f'{frame_id_counter}, {object_id_counter}, {x}, {y}, {w}, {h}, 1, 1, 1\n'
                                print(f'{frame_id_counter}, {object_id_counter}, {x}, {y}, {w}, {h}, 1, 1, 1')
                                f.write(mot_line)

                                frame_id_counter += 1

                        print(f'object_id_counter: {object_id_counter}')

    print("conversion to gt.txt complete.")


if __name__ == '__main__':
    generate_mot_file()


