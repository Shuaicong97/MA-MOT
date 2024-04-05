import numpy as np
from pycocotools import mask as coco_mask
import json
import os
import time


def decode_segmentations(segmentations):
    boxes = []
    for segment in segmentations:
        # {segment['segmentations']} is like {'size': [1080, 1920], 'counts': 'PPYo1'}
        segmentation = segment['segmentations']
        # Decode RLE format to binary mask
        mask = coco_mask.decode(segmentation)

        # Ture if in the mask there is at least one non-zero value.
        if np.any(mask):
            # Calculate bounding box from mask
            # NOTE: bbox.size > 0 is always true
            bbox = np.argwhere(mask)
            xmin = np.min(bbox[:, 1])
            xmax = np.max(bbox[:, 1])
            ymin = np.min(bbox[:, 0])
            ymax = np.max(bbox[:, 0])

            # Append bounding box coordinates to the list
            boxes.append([segment['frame'], segment['obj_id'], xmin, ymin, xmax - xmin, ymax - ymin,
                          segment['score'], 1, 1])

    return boxes


def save_to_file(decoded_segmentations, foldername, filename):
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    filepath = os.path.join(foldername, filename)
    with open(filepath, 'w') as f:
        for segmentation in decoded_segmentations:
            f.write(' '.join(map(str, segmentation)) + '\n')


def process_json_file(json_file):
    print(f'Program starts!')

    start_time = time.time()
    with open(json_file, 'r') as f:
        data = json.load(f)

    video_segmentations = {}
    obj_id = 1

    for item in data:
        video_id = item['video_id']
        segmentations = item['segmentations']
        score = item['score']
        if video_id not in video_segmentations:
            video_segmentations[video_id] = []

        for index, segmentation in enumerate(segmentations):
            video_segmentations[video_id].append({'frame': index + 1, 'obj_id': obj_id,
                                                  'segmentations': segmentation, 'score': score})
        obj_id += 1

        if obj_id > 20:
            obj_id = 1

    for video_id, segments in video_segmentations.items():
        decoded_segmentations = decode_segmentations(segments)
        print(decoded_segmentations)
        save_to_file(decoded_segmentations, 'data/generated_by_code/dvis_bboxes/', f'{video_id}.txt')

    end_time = time.time()
    elapsed_time = end_time - start_time
    # Program completed! Elapsed time: 770.6677641868591 seconds
    print(f'Program completed! Elapsed time: {elapsed_time} seconds')


json_file = 'data/DVIS/output_DVIS_Plus_Offline_VitAdapterL_OVIS/inference/results.json'
# process_json_file(json_file)


def rename_gt_file_using_video_name():
    folder_path = 'data/generated_by_code/dvis_ovis_video_gt'
    file_names = os.listdir(folder_path)

    with open('data/OVIS/annotations_valid.json', 'r') as f:
        data = json.load(f)

    videos = data['videos']
    for video in videos:
        video_id = video['id']
        file_names_array = video['file_names']
        video_file_name = str(video_id) + '.txt'
        if video_file_name in file_names:
            folder_name = file_names_array[0].split('/')[0]
            old_file_path = os.path.join(folder_path, str(video_id) + '.txt')
            new_file_name = folder_name + '.txt'
            new_file_path = os.path.join(folder_path, new_file_name)

            os.rename(old_file_path, new_file_path)


rename_gt_file_using_video_name()


