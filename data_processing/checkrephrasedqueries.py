import json

# 文件路径
file_mot17_training_re_path = '../data/Ours/MOT17-training_unique_language_queries_rephrased.txt'
file_mot17_training_path = '../data/Ours/MOT17-training_unique_language_queries.txt'
output_mot17_training_path = '../data/Ours/MOT17-training_combined_language_queries.json'

file_mot17_valid_re_path = '../data/Ours/MOT17-valid_unique_language_queries_rephrased.txt'
file_mot17_valid_path = '../data/Ours/MOT17-valid_unique_language_queries.txt'
output_mot17_valid_path = '../data/Ours/MOT17-valid_combined_language_queries.json'

file_mot20_training_re_path = '../data/Ours/MOT20-training_unique_language_queries_rephrased.txt'
file_mot20_training_path = '../data/Ours/MOT20-training_unique_language_queries.txt'
output_mot20_training_path = '../data/Ours/MOT20-training_combined_language_queries.json'

file_mot20_valid_re_path = '../data/Ours/MOT20-valid_unique_language_queries_rephrased.txt'
file_mot20_valid_path = '../data/Ours/MOT20-valid_unique_language_queries.txt'
output_mot20_valid_path = '../data/Ours/MOT20-valid_combined_language_queries.json'

file_ovis_training_re_path = '../data/Ours/OVIS-training_unique_language_queries_rephrased.txt'
file_ovis_training_path = '../data/Ours/OVIS-training_unique_language_queries.txt'
output_ovis_training_path = '../data/Ours/OVIS-training_combined_language_queries.json'

file_ovis_valid_re_path = '../data/Ours/OVIS-valid_unique_language_queries_rephrased.txt'
file_ovis_valid_path = '../data/Ours/OVIS-valid_unique_language_queries.txt'
output_ovis_valid_path = '../data/Ours/OVIS-valid_combined_language_queries.json'


def compare_files_and_store_json(file_a, file_b, output_file):
    # 读取文件a和b的内容
    with open(file_a, 'r', encoding='utf-8') as fa, open(file_b, 'r', encoding='utf-8') as fb:
        lines_a = fa.readlines()
        lines_b = fb.readlines()

    # 创建一个空列表用于存储json数据
    result = []

    # 获取两个文件的最大行数
    max_lines = max(len(lines_a), len(lines_b))

    # 遍历每一行
    for i in range(max_lines):
        # 获取a文件和b文件的对应行内容
        line_a = lines_a[i].strip() if i < len(lines_a) else ""
        line_b = lines_b[i].strip() if i < len(lines_b) else ""

        # 将行数、a的内容、b的内容存储到result列表中
        result.append({
            "line_number": i + 1,
            "rephrased_content": line_a,
            "original_content": line_b
        })

    # 将结果存储到json文件中
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)


# # 不再使用，因为后续combine文件有人工修改
# compare_files_and_store_json(file_mot17_training_re_path, file_mot17_training_path, output_mot17_training_path)
# compare_files_and_store_json(file_mot17_valid_re_path, file_mot17_valid_path, output_mot17_valid_path)
# compare_files_and_store_json(file_mot20_training_re_path, file_mot20_training_path, output_mot20_training_path)
# compare_files_and_store_json(file_mot20_valid_re_path, file_mot20_valid_path, output_mot20_valid_path)
# compare_files_and_store_json(file_ovis_training_re_path, file_ovis_training_path, output_ovis_training_path)
# compare_files_and_store_json(file_ovis_valid_re_path, file_ovis_valid_path, output_ovis_valid_path)


def add_new_item(data_type, a_item, new_a_data, rephrased):
    if data_type == 'mot17':
        new_item = {
            "Video": a_item['Video'],
            "Query ID": a_item['Query ID'],
            "Language Query": rephrased,
            "Type": a_item['Type'],
            "Track ID": a_item['Track ID'],
            "Start Frame": a_item['Start Frame'],
            "End Frame": a_item['End Frame'],
            "Revision": a_item['Revision']
        }
        new_a_data.append(new_item)

    if data_type == 'mot20':
        new_item = {
            "Video": a_item['Video'],
            "Query ID": a_item['Query ID'],
            "Language Query": rephrased,
            "Type": a_item['Type'],
            "IDs": a_item['IDs'],
            "Start": a_item['Start'],
            "End": a_item['End'],
            "Revision": a_item['Revision']
        }
        new_a_data.append(new_item)

    if data_type == 'ovis training':
        new_item = {
            "Video": a_item['Video'],
            "QID": a_item['QID'],
            "Language Query": rephrased,
            "Type": a_item['Type'],
            "IDs": a_item['IDs'],
            "Start": a_item['Start'],
            "End": a_item['End'],
            "Revision": a_item['Revision']
        }
        new_a_data.append(new_item)

    if data_type == 'ovis valid':
        new_item = {
            "ID mark frame": a_item['ID mark frame'],
            "Video": a_item['Video'],
            "QID": a_item['QID'],
            "Language Query": rephrased,
            "Type": a_item['Type'],
            "IDs": a_item['IDs'],
            "Start": a_item['Start'],
            "End": a_item['End'],
            "Revision": a_item['Revision']
        }
        new_a_data.append(new_item)


def combine_queries(data_type, info_json, rephrased_json, output_json):
    with open(info_json, 'r') as file_a, open(rephrased_json, 'r') as file_b:
        a_data = json.load(file_a)
        b_data = json.load(file_b)

    # 遍历 A.json 数据
    new_a_data = []
    for a_item in a_data:
        original_query = a_item['Language Query']

        # 查找 B.json 中的对应内容
        matched_rephrased = None
        for b_item in b_data:
            if b_item['original_content'] == original_query:
                matched_rephrased = b_item['rephrased_content']

                if 'extra_rephrased' in b_item:
                    for extra_rephrased_item in b_item['extra_rephrased']:
                        if extra_rephrased_item:
                            add_new_item(data_type, a_item, a_data, extra_rephrased_item)
                break

        # 保留原始对象
        new_a_data.append(a_item)

        # 如果找到了匹配的 rephrased_content，创建新的对象
        if matched_rephrased:
            add_new_item(data_type, a_item, a_data, matched_rephrased)

    # 保存新的数据到新的 JSON 文件
    with open(output_json, 'w') as file_a_updated:
        json.dump(new_a_data, file_a_updated, indent=4)

    print(f"更新完成，已保存为{output_json}")


combine_queries('mot17', '../data/Ours/MOT17-training.json', 'rephrase_queries/MOT17-training_combined_language_queries.json', 'rephrase_queries/MOT17-training-doubled.json')
combine_queries('mot17', '../data/Ours/MOT17-valid.json', 'rephrase_queries/MOT17-valid_combined_language_queries.json', 'rephrase_queries/MOT17-valid-doubled.json')
combine_queries('mot20', '../data/Ours/MOT20-training.json', 'rephrase_queries/MOT20-training_combined_language_queries.json', 'rephrase_queries/MOT20-training-doubled.json')
combine_queries('mot20', '../data/Ours/MOT20-valid.json', 'rephrase_queries/MOT20-valid_combined_language_queries.json', 'rephrase_queries/MOT20-valid-doubled.json')
combine_queries('ovis training', '../data/Ours/OVIS-training.json', 'rephrase_queries/OVIS-training_combined_language_queries.json', 'rephrase_queries/OVIS-training-doubled.json')
combine_queries('ovis valid', '../data/Ours/OVIS-valid.json', 'rephrase_queries/OVIS-valid_combined_language_queries.json', 'rephrase_queries/OVIS-valid-doubled.json')

