import os
import json

# 读取 JSON 文件
def load_json(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def clear_output_directory(output_base):
    if os.path.exists(output_base):
        for root, dirs, files in os.walk(output_base, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(output_base)
    os.makedirs(output_base, exist_ok=True)


def process_special_video(video_name, start, end):
    # train set 84 不连续 1-13, 15-85
    if video_name == "2fb5a55b":
        if start >= 15:
            start = start - 1
        if end >= 15:
            end = end - 1
    # train set 342 不连续 1-70, 72, 89-359
    if video_name == "86a88668":
        if start == 72:
            start = start - 1
        if end == 72:
            end = end - 1

        if start >= 89:
            start = start - 17
        if end >= 89:
            end = end - 17
    # valid set 231 不连续 1-5, 8, 12-236
    if video_name == "af48b2f9":
        if start == 8:
            start = start - 2
        if end == 8:
            end = end - 2

        if start >= 12:
            start = start - 5
        if end >= 12:
            end = end - 5
    # valid set 164 未从1开始 171-334
    if video_name == "cfff47c3":
        start = start - 170
        end = end - 170

    return start, end

# annotation_file里的Start, End根据img名字来，gt.txt根据bboxes长度来（连续）。因此对于不连续的视频需要转换获取正确的box
def generate_gt_per_query(annotation_file, gt_folder, output_base):
    os.makedirs(output_base, exist_ok=True)
    data = load_json(annotation_file)
    clear_output_directory(output_base)

    # 遍历 JSON 数据
    for item in data:
        video = item["Video"]
        language_query = item["Language Query"].lower().replace(" ", "-")
        ids = str(item["IDs"])
        start = int(item["Start"])
        end = int(item["End"])
        start, end = process_special_video(video, start, end)

        video_folder = os.path.join(gt_folder, video)
        gt_file = os.path.join(video_folder, "gt.txt")
        output_folder = os.path.join(output_base, video, language_query)
        output_file = os.path.join(output_folder, "gt.txt")

        if not os.path.exists(gt_file):
            print(f"[WARNING] gt.txt not found for {video}, skipping...")
            continue

        os.makedirs(output_folder, exist_ok=True)

        # 读取 GT 文件并筛选符合条件的行
        with open(gt_file, "r", encoding="utf-8") as gt_f:
            gt_lines = gt_f.readlines()

        filtered_lines = []
        for line in gt_lines:
            parts = line.strip().split(", ")
            if len(parts) < 6:
                continue

            frame_id = int(parts[0])
            track_id = parts[1]

            if start <= frame_id <= end and track_id == ids:
                filtered_lines.append(line)

        # 确保不会覆盖已有内容，而是追加写入
        with open(output_file, "a", encoding="utf-8") as out_f:
            out_f.writelines(filtered_lines)

        # print(f"Processed {output_file}")

    print("All done!")

generate_gt_per_query("/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-training-doubled.json",
                      "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS_GTs/train",
                      "ovis-gt/train" )
generate_gt_per_query("/Users/shuaicongwu/PycharmProjects/data_processing/Rephrased data/OVIS-valid-doubled.json",
                      "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS_GTs/val",
                      "ovis-gt/valid" )







