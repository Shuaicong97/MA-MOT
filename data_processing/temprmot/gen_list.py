# import json
# import os
#
# # 有些官方OVIS training video我们没有使用
# # 读取 JSON 文件
# with open("/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training-videos-name.json", "r", encoding="utf-8") as f:
#     valid_names = set(json.load(f))  # 使用集合提高查找效率
#
# # 指定要遍历的目录
# directory = "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/ovis/train/JPEGImages"
#
# # 获取 A 目录下的所有文件夹
# all_folders = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
#
# # 查找在 a.json 里没有的文件夹
# not_found = [folder for folder in all_folders if folder not in valid_names]
#
# # 输出找不到匹配项的文件夹
# for folder in not_found:
#     print(folder)

import os

# 定义目标目录
directory_A = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/refer-ovis/OVIS/labels_with_ids'

# 用于保存文件路径的列表
txt_files = []

# 遍历目录及其子目录
for root, dirs, files in os.walk(directory_A):
    for file in files:
        if file.endswith('.txt'):  # 判断是否是 txt 文件
            # 获取从 OVIS 开始的路径部分
            relative_path = os.path.relpath(root, directory_A)
            full_path = os.path.join('OVIS', relative_path, file)
            txt_files.append(full_path)  # 保存从 OVIS 开始的文件路径

txt_files.sort(key=lambda x: (x.split('/')[1], int(x.split('/')[-1].split('.')[0])))

# 将所有文件路径写入 refer-ovis.train 文件
with open('refer-ovis.train', 'w') as f:
    for txt_file in txt_files:
        adjusted_path = txt_file.replace('OVIS/', 'OVIS/training/').replace('.txt', '.jpg')
        f.write(adjusted_path + '\n')

print("所有txt文件路径已保存至 'refer-ovis.train' 文件中。")

