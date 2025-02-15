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
# try:
#     with open(output_file, "w") as f:
#         for folder_path in folder_paths:
#             if not os.path.exists(folder_path):
#                 print(f"路径不存在: {folder_path}")
#                 continue
#
#             folder_name = os.path.basename(folder_path)
#             json_files = [file for file in os.listdir(folder_path) if file.endswith('.json')]
#             for file_name in json_files:
#                 name_without_extension = os.path.splitext(file_name)[0]
#                 f.write(f"{folder_name}+{name_without_extension}\n")
#     print(f"文件 {output_file} 已成功创建！")
# except Exception as e:
#     print(f"发生错误: {e}")

def save_json_filenames(root_dir, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for folder_name in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder_name)
            if os.path.isdir(folder_path):  # 确保是文件夹
                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.json'):
                        name_without_extension = os.path.splitext(file_name)[0]
                        entry = f"{folder_name}+{name_without_extension}\n"
                        f.write(entry)

# 使用示例
root_directory = "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/refer-ovis/expression/valid"
output_file = "seqmap_ovis.txt"
save_json_filenames(root_directory, output_file)
