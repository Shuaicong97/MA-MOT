import json
import os

# 读取 JSON 文件
with open("/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/temprmot/video_info_valid.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 计算 file_name 的总数
file_count = len(data)

print("file_name 总数:", file_count)

file_names = {item["file_name"] for item in data}
print("所有 file_name:", file_names)

# 获取目录 a 下的文件夹列表
a_path = "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS_valid"  # 目录路径，根据实际情况修改
existing_folders = {folder for folder in os.listdir(a_path) if os.path.isdir(os.path.join(a_path, folder))}

# 找出缺失的文件夹
missing_folders = file_names - existing_folders

# 输出缺失的文件夹
print("缺失的文件夹数量:", len(missing_folders))
print("缺失的文件夹:", missing_folders)

