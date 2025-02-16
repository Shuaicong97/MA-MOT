import csv
from collections import defaultdict


def find_duplicates(csv_file):
    video_data = defaultdict(lambda: {'annotation_ids': set(), 'ovis_ids': set(), 'duplicates': []})

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头

        for row in reader:
            video_id, annotation_id, ovis_id = row[0], row[1], row[2]

            if annotation_id in video_data[video_id]['annotation_ids']:
                video_data[video_id]['duplicates'].append(("Annotation ID", annotation_id))
            if ovis_id in video_data[video_id]['ovis_ids']:
                video_data[video_id]['duplicates'].append(("Ovis ID (DVIS)", ovis_id))

            video_data[video_id]['annotation_ids'].add(annotation_id)
            video_data[video_id]['ovis_ids'].add(ovis_id)

    for video_id, data in video_data.items():
        if data['duplicates']:
            print(f"Video ID: {video_id}")
            for dup_type, dup_value in data['duplicates']:
                print(f"  Duplicate {dup_type}: {dup_value}")


# 调用函数，替换 'your_file.csv' 为实际的 CSV 文件路径
find_duplicates('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/temprmot/Id conversion - Our OVIS valid set.csv')
