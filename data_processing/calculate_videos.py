import json


# 假设文件名分别为 file1.json 和 file2.json
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)


def count_different_videos(file1, file2):
    # 读取两个JSON文件
    data1 = load_json(file1)
    data2 = load_json(file2)

    # 提取并去重两个文件中的Video值
    videos1 = {item["Video"] for item in data1}  # 使用集合去重
    videos2 = {item["Video"] for item in data2}  # 使用集合去重

    # 求两个集合的差集，得到不同的Video值
    different_videos = videos1.symmetric_difference(videos2)

    # 返回不同Video值的数量
    return len(different_videos)


# 调用函数，假设文件名为 file1.json 和 file2.json
file1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training.json'
file2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid.json'

result = count_different_videos(file1, file2)
print(f"两个文件中不同Video值的总数是: {result}")
