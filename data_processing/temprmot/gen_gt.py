import os
import json

# 输入目录路径
gt_train_dir = "../../data/MOT20/train"  # 替换为实际目录a路径
info_json_path = "mot_video_info.json"  # 替换为实际b.json路径
output_dir = "../../data/refer-mot20/MOT20/labels_with_ids"  # 替换为目标输出路径


# 加载 b.json 数据
with open(info_json_path, "r") as f:
    b_data = json.load(f)

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 遍历目录a中的所有子文件夹
for folder_name in os.listdir(gt_train_dir):
    folder_path = os.path.join(gt_train_dir, folder_name)
    if not os.path.isdir(folder_path):
        continue

    # 在 b.json 中匹配 file_name
    matched_entry = next((entry for entry in b_data if entry["file_name"] == folder_name), None)
    if not matched_entry:
        print(f"文件夹 {folder_name} 在 b.json 中未匹配，跳过。")
        continue

    # 获取 width 和 height
    width = matched_entry["width"]
    height = matched_entry["height"]

    # 读取 gt.txt 文件
    gt_file_path = os.path.join(folder_path, "gt/gt.txt")
    if not os.path.isfile(gt_file_path):
        print(f"{gt_file_path} 文件不存在，跳过。")
        continue

    # 创建对应的输出子目录
    output_subdir = os.path.join(output_dir, folder_name)
    os.makedirs(output_subdir, exist_ok=True)

    # 处理 gt.txt 文件
    frame_data = {}
    with open(gt_file_path, "r") as gt_file:
        for line in gt_file:
            # 提取数据行的前六个字段
            frame_id, obj_id, x, y, w, h, *_ = map(float, line.strip().split(","))
            frame_id = int(frame_id)
            obj_id = int(obj_id)

            # 归一化并格式化数据
            x_normalized = round(x / width, 6)
            y_normalized = round(y / height, 6)
            w_normalized = round(w / width, 6)
            h_normalized = round(h / height, 6)

            # 构建输出数据行
            formatted_line = f"0 {obj_id} {x_normalized:.6f} {y_normalized:.6f} {w_normalized:.6f} {h_normalized:.6f}\n"

            # 将数据加入对应 frame_id 的列表
            if frame_id not in frame_data:
                frame_data[frame_id] = []
            frame_data[frame_id].append(formatted_line)

    # 写入输出文件
    for frame_id, lines in frame_data.items():
        output_file_path = os.path.join(output_subdir, f"{frame_id:06}.txt")
        with open(output_file_path, "w") as output_file:
            output_file.writelines(lines)

    print(f"处理完成：{folder_name}")

print(f"所有文件处理完成，结果保存在 {output_dir}。")
