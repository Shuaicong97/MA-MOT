import os
import json
import shutil


# 假设文件路径和目标目录
input_ovis_training_file = "../../data/Ours/OVIS-training.json"
output_ovis_training_path = "../../data/refer-ovis/expression/training"
input_ovis_valid_file = "../../data/Ours/OVIS-valid.json"
output_ovis_valid_path = "../../data/refer-ovis/expression/valid"

def clear_folder(folder_path):
    # 检查文件夹是否存在
    if not os.path.exists(folder_path):
        print(f"路径 {folder_path} 不存在")
        return

    # 遍历文件夹中的所有内容
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # 如果是文件夹，递归删除
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        # 如果是文件，直接删除
        elif os.path.isfile(file_path):
            os.remove(file_path)

    print(f"已清空文件夹：{folder_path}")

clear_folder(output_ovis_training_path)
clear_folder(output_ovis_valid_path)

def gen_original_json(input_f, output):
    with open(input_f, "r", encoding="utf-8") as f:
        data = json.load(f)

    label_dict = {}

    # 遍历数据并生成文件
    for entry in data:
        video_name = entry["Video"]
        language_query = entry["Language Query"]
        start = int(entry["Start"])
        end = int(entry["End"])
        ids = int(entry["IDs"])

        # 创建视频文件夹
        video_path = os.path.join(output, video_name)
        os.makedirs(video_path, exist_ok=True)

        # 生成文件名（小写并用-连接）
        file_name = language_query.lower().replace(" ", "-") + ".json"
        file_path = os.path.join(video_path, file_name)

        # 生成 frame_id 对应的 object_ids 映射
        if file_path not in label_dict:
            label_dict[file_path] = {}

        for frame in range(start, end + 1):
            frame_str = str(frame)
            if frame_str not in label_dict[file_path]:
                label_dict[file_path][frame_str] = []
            if ids not in label_dict[file_path][frame_str]:
                label_dict[file_path][frame_str].append(ids)

    for file_path, labels in label_dict.items():
        # 生成 JSON 内容
        json_content = {
            "label": labels,
            "ignore": {},
            "video_name": os.path.basename(os.path.dirname(file_path)),
            "sentence": " ".join(os.path.splitext(os.path.basename(file_path))[0].split("-")).capitalize()
        }

        # 写入 JSON 文件
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_content, f, ensure_ascii=False, indent=None, separators=(', ', ': '))

    print("所有 JSON 文件已生成！")

gen_original_json(input_ovis_training_file, output_ovis_training_path)
gen_original_json(input_ovis_valid_file, output_ovis_valid_path)


def gen_rephrased_json(input_f, output):
    with open(input_f, "r", encoding="utf-8") as f:
        data = json.load(f)

    label_dict = {}
    # 遍历数据并生成文件
    for entry in data:
        video_name = entry["Video"]
        language_query = entry["Language Query"]
        start = int(entry["Start"])
        end = int(entry["End"])
        ids = int(entry["IDs"])
        raw_sentence = entry["Raw sentence"]

        # 创建视频文件夹
        video_path = os.path.join(output, video_name)
        os.makedirs(video_path, exist_ok=True)

        # 生成文件名（小写并用-连接）
        file_name = language_query.lower().replace(" ", "-") + ".json"
        file_path = os.path.join(video_path, file_name)

        # 生成 frame_id 对应的 object_ids 映射
        if file_path not in label_dict:
            label_dict[file_path] = {
                "labels": {},  # 存储 frame_id -> object_ids 的映射
                "raw_sentence": raw_sentence  # 存储对应的 raw_sentence
            }

        for frame in range(start, end + 1):
            frame_str = str(frame)
            if frame_str not in label_dict[file_path]["labels"]:
                label_dict[file_path]["labels"][frame_str] = []
            if ids not in label_dict[file_path]["labels"][frame_str]:
                label_dict[file_path]["labels"][frame_str].append(ids)

    for file_path, file_data in label_dict.items():
        labels = file_data["labels"]
        raw_sentence = file_data["raw_sentence"]
        # 生成 JSON 内容
        json_content = {
            "label": labels,
            "ignore": {},
            "video_name": os.path.basename(os.path.dirname(file_path)),
            "sentence": " ".join(os.path.splitext(os.path.basename(file_path))[0].split("-")).capitalize(),
            "raw_sentence": raw_sentence
        }

        # 写入 JSON 文件
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(json_content, f, ensure_ascii=False, indent=None, separators=(', ', ': '))

    print("Rephrased内容生成！")

gen_rephrased_json('unique_objects_ovis-training.json', output_ovis_training_path)
gen_rephrased_json('unique_objects_ovis-valid.json', output_ovis_valid_path)

