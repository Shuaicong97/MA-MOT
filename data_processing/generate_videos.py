import csv
import json
from collections import defaultdict

def check_validation(csv_path, video_rows, valid_videos):
    # 第一步：把所有行按 Video 分组
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            video = row.get("Video", "").strip()
            video_rows[video].append(row)

    # 第二步：遍历每个 video 组，判断是否合法
    for video, rows in video_rows.items():
        has_valid_start_end = any(row.get("Start") and row.get("End") for row in rows)

        if not has_valid_start_end:
            print(f"[跳过] Video '{video}' 没有任何一行包含 Start 和 End，有缺失。")
            continue

        valid_videos.add(video)

def extract_unique_videos(csv_path_1, csv_path_2, output_txt_path):
    video_rows = defaultdict(list)
    valid_videos = set()

    check_validation(csv_path_1, video_rows, valid_videos)
    check_validation(csv_path_2, video_rows, valid_videos)

    # 保存为 txt 文件，每个视频 ID 一行
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for video_id in valid_videos:
            f.write(video_id + '\n')

    print(f"\n✅ 共提取 {len(valid_videos)} 个合法 Video，并保存到 {output_txt_path}")
    return valid_videos

# 示例调用
extract_unique_videos("/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS(Ashiq).csv",
                      "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS(Seenat).csv",
                      "report/ovis_info_train_533.txt")
extract_unique_videos("/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS-Test(Ashiq).csv",
                      "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS-Test(Seenat).csv",
                      "report/ovis_info_valid_137.txt")
