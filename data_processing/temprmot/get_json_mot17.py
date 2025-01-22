import os
import json
from collections import defaultdict

# 读取原始的JSON数据文件
input_mot17_training_file = "../../data/Ours/MOT17-training.json"
output_mot17_training_path = "../../data/refer-mot17/expression"
input_mot17_valid_file = "../../data/Ours/MOT17-valid.json"

def gen_original_json(input_file, output_dir):
    with open(input_file, 'r') as f:
        data = json.load(f)

    # 按 Language Query 分组数据
    query_groups = defaultdict(list)
    for entry in data:
        query_groups[entry['Language Query']].append(entry)

    # 遍历分组数据，生成需要的JSON文件
    for language_query, entries in query_groups.items():
        # 获取共同的属性
        video_name = entries[0]['Video']

        # 合并所有的 Track ID 和时间范围
        label = defaultdict(list)
        for entry in entries:
            try:
                # 过滤掉无法转换为整数的 Track ID
                track_ids = [
                    int(item) for item in entry['Track ID'].split(',') if item.isdigit()
                ]
            except ValueError:
                # 跳过无效的条目
                continue
            start_frame = int(entry['Start Frame'])
            end_frame = int(entry['End Frame'])
            for frame_id in range(start_frame, end_frame + 1):
                label[str(frame_id)].extend(track_ids)

        # 确保每个帧的Track ID是唯一的
        label = {k: sorted(set(v)) for k, v in sorted(label.items(), key=lambda item: int(item[0]))}

        # 生成JSON文件名（小写且用-连接）
        json_file_name = language_query.lower().replace(' ', '-').replace(',', '') + '.json'

        # 创建输出目录
        video_dir = os.path.join(output_dir, video_name)
        os.makedirs(video_dir, exist_ok=True)

        # 构造最终的JSON结构
        output_data = {
            "label": {k: sorted(v) for k, v in label.items()},
            "ignore": [],
            "video_name": video_name,
            "sentence": language_query
        }

        # 写入JSON文件
        output_path = os.path.join(video_dir, json_file_name)
        with open(output_path, 'w') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=None, separators=(', ', ': '))

    print("Processing complete! Check the 'expression' directory for results.")

def gen_rephrased_json(input_file, output_dir):
    with open(input_file, 'r') as f:
        data = json.load(f)

    # 按 Language Query 分组数据
    query_groups = defaultdict(list)
    for entry in data:
        query_groups[entry['Language Query']].append(entry)

    # 遍历分组数据，生成需要的JSON文件
    for language_query, entries in query_groups.items():
        # 获取共同的属性
        video_name = entries[0]['Video']
        raw_sentence = entries[0]['Raw sentence']

        # 合并所有的 Track ID 和时间范围
        label = defaultdict(list)
        for entry in entries:
            try:
                # 过滤掉无法转换为整数的 Track ID
                track_ids = [
                    int(item) for item in entry['IDs'].split(',') if item.isdigit()
                ]
            except ValueError:
                # 跳过无效的条目
                continue
            start_frame = int(entry['Start'])
            end_frame = int(entry['End'])
            for frame_id in range(start_frame, end_frame + 1):
                label[str(frame_id)].extend(track_ids)

        # 确保每个帧的Track ID是唯一的
        label = {k: sorted(set(v)) for k, v in sorted(label.items(), key=lambda item: int(item[0]))}

        # 生成JSON文件名（小写且用-连接）
        json_file_name = language_query.lower().replace(' ', '-').replace(',', '') + '.json'

        # 创建输出目录
        video_dir = os.path.join(output_dir, video_name)
        os.makedirs(video_dir, exist_ok=True)

        # 构造最终的JSON结构
        output_data = {
            "label": {k: sorted(v) for k, v in label.items()},
            "ignore": [],
            "video_name": video_name,
            "sentence": language_query,
            "raw_sentence": raw_sentence
        }

        # 写入JSON文件
        output_path = os.path.join(video_dir, json_file_name)
        with open(output_path, 'w') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=None, separators=(', ', ': '))

    print("Processing of rephrased complete! Check the 'expression' directory for results.")

gen_original_json(input_mot17_training_file, output_mot17_training_path)
gen_rephrased_json('unique_objects_mot17-training.json', output_mot17_training_path)

gen_original_json(input_mot17_valid_file, output_mot17_training_path)
gen_rephrased_json('unique_objects_mot17-valid.json', output_mot17_training_path)

# input_mot20_training_file = "../../data/Ours/MOT20-training.json"
# input_mot20_valid_file = "../../data/Ours/MOT20-valid.json"
# output_mot20_path = "../../data/refer-mot20/expression"
#
# gen_original_json(input_mot20_training_file, output_mot20_path)
# gen_rephrased_json('unique_objects_mot20-training.json', output_mot20_path)
#
# gen_original_json(input_mot20_valid_file, output_mot20_path)
# gen_rephrased_json('unique_objects_mot20-valid.json', output_mot20_path)


