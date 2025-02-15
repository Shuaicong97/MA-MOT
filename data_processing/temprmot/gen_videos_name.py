import os

folder_path = "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/refer-ovis/expression/valid"
subfolders = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]

print(subfolders)
print("子文件夹总数:", len(subfolders))