import json

# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 加载数据
name_list = load_json('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training-videos-name.json')  # 假设 name.json 是一个列表
info_list = load_json('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/temprmot/video_info_train.json')  # 假设 info.json 是一个列表，包含字典
name_list2 = load_json('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid-videos-name.json')  # 假设 name.json 是一个列表
info_list2 = load_json('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/temprmot/video_info_valid.json')  # 假设 info.json 是一个列表，包含字典

# 提取 info.json 中的 file_name 集合，提高查找效率
file_names = {item['file_name'] for item in info_list2}

# 遍历 name.json 并检查是否匹配
for name in name_list2:
    if name not in file_names:
        print(f'没有匹配项: {name}')
