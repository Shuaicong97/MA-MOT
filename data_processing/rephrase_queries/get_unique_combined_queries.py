import json

def get_unique_combined_queries(input_file, output_file):
    # 读取原始 JSON 数据
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # 用于存储唯一的 original_content 对应的数据
    unique_entries = {}

    # 遍历数据，确保每个 original_content 只保留一条记录
    for entry in data:
        original_content = entry["original_content"]
        if original_content not in unique_entries:
            unique_entries[original_content] = entry

    # 获取去重后的数据
    unique_data = list(unique_entries.values())

    # 重新排序 line_number，从 1 开始
    for idx, entry in enumerate(unique_data, start=1):
        entry["line_number"] = idx

    # 将去重并重新排序后的数据写入新的 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(unique_data, file, ensure_ascii=False, indent=4)

    print(f"去重并重新排序后的数据已保存到 {output_file}")

get_unique_combined_queries('../../data/Ours/MOT17-training_combined_language_queries.json', 'MOT17-training_combined_language_queries.json')
get_unique_combined_queries('../../data/Ours/MOT17-valid_combined_language_queries.json', 'MOT17-valid_combined_language_queries.json')
get_unique_combined_queries('../../data/Ours/MOT20-training_combined_language_queries.json', 'MOT20-training_combined_language_queries.json')
get_unique_combined_queries('../../data/Ours/MOT20-valid_combined_language_queries.json', 'MOT20-valid_combined_language_queries.json')
get_unique_combined_queries('../../data/Ours/OVIS-training_combined_language_queries.json', 'OVIS-training_combined_language_queries.json')
get_unique_combined_queries('../../data/Ours/OVIS-valid_combined_language_queries.json', 'OVIS-valid_combined_language_queries.json')