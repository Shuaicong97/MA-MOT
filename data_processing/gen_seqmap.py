import os

# 定义文件夹路径和输出文件名
folder_paths = [
    '../data/refer-mot17/expression/MOT17-01',
    '../data/refer-mot17/expression/MOT17-03',
    '../data/refer-mot17/expression/MOT17-06',
    '../data/refer-mot17/expression/MOT17-07',
    '../data/refer-mot17/expression/MOT17-08',
    '../data/refer-mot17/expression/MOT17-12',
    '../data/refer-mot17/expression/MOT17-14'
]
output_file = "seqmap_mot17.txt"

folder_paths = [
    '../data/refer-mot20/expression/MOT20-03',
    '../data/refer-mot20/expression/MOT20-05'
]
output_file = "seqmap_mot20.txt"

# 遍历文件夹，获取所有json文件名
try:
    with open(output_file, "w") as f:
        for folder_path in folder_paths:
            if not os.path.exists(folder_path):
                print(f"路径不存在: {folder_path}")
                continue

            folder_name = os.path.basename(folder_path)
            json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
            for file_name in json_files:
                name_without_extension = os.path.splitext(file_name)[0]
                f.write(f"{folder_name}+{name_without_extension}\n")
    print(f"文件 {output_file} 已成功创建！")
except Exception as e:
    print(f"发生错误: {e}")
