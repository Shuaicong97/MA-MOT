import json
import os

def get_boxes():
    # 读取 a.json 文件
    file_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/annotations_train.json'  # 请确保路径正确
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 提取 video_id = 28 的所有 annotation
    annotations_with_video_id_29 = [annotation for annotation in data['annotations'] if annotation['video_id'] == 29]

    # 创建输出目录
    output_dir = 'video_29_bboxes'
    os.makedirs(output_dir, exist_ok=True)

    # 遍历每个 annotation，提取并保存 bboxes 信息
    for annotation in annotations_with_video_id_29:
        annotation_id = annotation['id']
        bboxes = annotation['bboxes']

        # 构建保存数据
        result = {
            "annotation_id": annotation_id,
            "video_id": annotation['video_id'],
            "bboxes": bboxes
        }

        # 构建保存路径并写入文件
        output_file_path = os.path.join(output_dir, f'annotation_{annotation_id}_bboxes.json')
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(result, output_file, ensure_ascii=False)

    print(f"所有 Video ID = 29 的 bboxes 信息已保存到 {output_dir} 目录中。")


# 指定包含 JSON 文件的目录
folder_path = 'video_29_bboxes'  # 替换为实际目录路径

# 遍历文件夹中的所有 JSON 文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):  # 只处理 JSON 文件
        file_path = os.path.join(folder_path, file_name)

        # 读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 获取 bboxes 并计算长度
        bboxes = data.get('bboxes', [])
        bboxes_length = len(bboxes)

        # 输出结果
        print(f"文件: {file_name}, bboxes 的长度（包含 null）: {bboxes_length}")