import os
import csv

# 定义路径
root_dir = "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Filtered Results by Annotation"  # 根目录，包含多个 video_name 文件夹
output_dir = "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/temprmot/id_conversion_gt"  # 处理后文件的存储目录
csv_file = "Id conversion - Our OVIS valid set.csv"  # CSV 数据文件路径

# 读取 CSV，创建 { (video_id, ovis_id) -> annotation_id } 映射
id_mapping = {}
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)  # 跳过表头
    for row in reader:
        video_id, annotation_id, ovis_id = row[0], int(row[1]), int(row[2])
        id_mapping[(video_id, ovis_id)] = annotation_id  # 例如 (0d0030a7, 3) -> 4

# 遍历 `a` 目录下的所有视频文件夹
for video_name in os.listdir(root_dir):
    video_path = os.path.join(root_dir, video_name, "gt", f"{video_name}.txt")

    if not os.path.isfile(video_path):
        continue  # 跳过无效文件

    new_lines = []

    # 读取原始文件
    with open(video_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 9:
                continue  # 跳过格式不对的行

            frame_id, object_id = int(parts[0]), int(parts[1])

            # 检查是否有匹配项
            key = (video_name, object_id)
            if key in id_mapping:
                parts[1] = str(id_mapping[key])  # 替换 object_id
                new_lines.append(parts)  # 这里存储列表形式，方便排序

    # 只有匹配到的行才写入新文件
    if new_lines:
        # 按第二列（object_id）排序，若相同则按第一列（frame_id）排序
        new_lines.sort(key=lambda x: (int(x[1]), int(x[0])))

        # 格式化并写入新文件
        output_path = os.path.join(output_dir, video_name)
        os.makedirs(output_path, exist_ok=True)  # 确保目录存在
        with open(os.path.join(output_path, f"{video_name}.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(" ".join(map(str, line)) for line in new_lines) + "\n")

print("处理完成！")
