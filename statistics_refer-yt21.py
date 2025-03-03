import json
from collections import defaultdict


# 读取 JSON 文件的函数
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# 统计唯一的 <video_id>
def count_unique_videos(file_paths):
    video_ids = set()

    for file_path in file_paths:
        data = load_json(file_path)
        if "videos" in data:
            video_ids.update(data["videos"].keys())
        print(file_path, "的 <video_id> 数量: ", len(video_ids))

    return len(video_ids)


# 统计 video_id 出现的文件
def find_duplicate_videos(file_paths):
    video_files = defaultdict(list)  # 记录 video_id 及其对应的文件

    for file_path in file_paths:
        data = load_json(file_path)
        if "videos" in data:
            for video_id in data["videos"].keys():
                video_files[video_id].append(file_path)  # 记录在哪些文件中出现

    # 找出重复的 video_id
    duplicate_videos = {video_id: files for video_id, files in video_files.items() if len(files) > 1}

    return duplicate_videos


# 假设文件路径为 file1.json, file2.json, file3.json
file_paths = ['data/Ref-YT/meta_expressions/test/meta_expressions.json',
         'data/Ref-YT/meta_expressions/train/meta_expressions.json',
         'data/Ref-YT/meta_expressions/valid/meta_expressions.json']
unique_video_count = count_unique_videos(file_paths)

print("不同的 <video_id> 数量总和: ", unique_video_count)

# duplicate_videos = find_duplicate_videos(file_paths)
# # 输出结果
# if duplicate_videos:
#     print("重复的 video_id 及其所在文件:")
#     for video_id, files in duplicate_videos.items():
#         print(f"{video_id}: 出现在 {files}")
# else:
#     print("没有重复的 video_id。")

# 计算去重后的 expressions 数量
def count_unique_expressions(file_paths):
    unique_expressions = set()  # 用于去重 (video_id, exp) 组合

    for file_path in file_paths:
        data = load_json(file_path)
        if "videos" in data:
            for video_id, video_data in data["videos"].items():
                if "expressions" in video_data:
                    for exp_data in video_data["expressions"].values():
                        exp_text = exp_data["exp"]
                        unique_expressions.add((video_id, exp_text))  # 存入 (video_id, exp) 组合

    return len(unique_expressions)


# 假设文件路径
unique_expression_count = count_unique_expressions(file_paths)

# 输出结果
print("去重后 expressions 的总数量:", unique_expression_count)  # 14952


# 计算去重后的 obj_id 数量
def count_unique_obj_ids(file_path):
    unique_obj_ids = set()  # 存储 (video_id, obj_id) 组合
    total_obj_ids = 0
    data = load_json(file_path)
    if "videos" in data:
        for video_id, video_data in data["videos"].items():
            if "expressions" in video_data:
                total_obj_ids += len(video_data["expressions"])
                for exp_data in video_data["expressions"].values():
                    obj_id = exp_data["obj_id"]
                    unique_obj_ids.add((video_id, obj_id))  # 记录 (video_id, obj_id)

    return len(unique_obj_ids), total_obj_ids

unique_obj_id_count, total_obj_ids = count_unique_obj_ids('data/Ref-YT/meta_expressions/train/meta_expressions.json')

# 输出结果
print("去重后 obj_id 的总数量:", unique_obj_id_count, ', ', total_obj_ids)


# 获取 JSON 文件的 key 集合
def get_json_keys(file_path):
    data = load_json(file_path)
    return set(data.keys())

# 读取 JSON 文件
ours_keys = get_json_keys("/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/verbs_json/verbs_ovis.json")
a_keys = get_json_keys("/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/verbs_json/verbs_hc-stvg.json")
b_keys = get_json_keys("/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/verbs_json/verbs_refer-yt.json")
c_keys = get_json_keys("/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/verbs_json/verbs_stvg.json")
d_keys = get_json_keys("/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/verbs_json/verbs_type2track.json")

# 计算在 a.json, b.json, c.json 任意一个文件中有，但 ours.json 没有的 key
missing_keys = (a_keys | b_keys | c_keys | d_keys) - ours_keys

# 输出结果
print("在 a.json, b.json, c.json 但不在 ours.json 的 key:", len(missing_keys), missing_keys)
