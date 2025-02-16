import os

# 设定文件夹路径
folder_a = "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/refer-ovis/expression/valid"  # 替换为实际路径

# 计算 JSON 文件的总数
json_count = 0

for root, _, files in os.walk(folder_a):
    json_count += sum(1 for file in files if file.endswith(".json"))

print(f"JSON 文件总数：{json_count}")
