import json
from pathlib import Path

# 输入 JSON 文件路径
input_json_path = "../../data/OVIS/annotations_train.json"
output_json_path = "video_info.json"

# 加载 JSON 文件
with open(input_json_path, "r") as f:
    data = json.load(f)

# 用于保存结果的列表
results = []

# 遍历 videos 列表
for video in data.get("videos", []):
    # 获取 width 和 height
    width = video.get("width")
    height = video.get("height")
    length = video.get("length")

    # 获取 file_names 的第一个路径
    file_names = video.get("file_names", [])
    if not file_names:
        continue

    # 提取父目录名（假设所有路径的父目录一致）
    first_file = file_names[0]
    parent_dir = Path(first_file).parent.name

    # 创建 JSON 对象
    result = {
        "width": width,
        "height": height,
        "file_name": parent_dir,
        "length": length
    }
    results.append(result)

# 保存结果为新的 JSON 文件
with open(output_json_path, "w") as f:
    json.dump(results, f, indent=4)

print(f"提取完成，结果已保存到 {output_json_path}")
