import json

# 修改输入数据中的 Language Query，将首字母改为大写，且删除末尾句号
def capitalize_and_clean(query):
    if query:
        # 首字母大写
        query = query[0].upper() + query[1:] if not query[0].isupper() else query
        # 删除末尾非字母字符
        while query and not query[-1].isalpha():
            query = query[:-1]
    return query

def get_unique_queries(input_file, output_file):
    # 从 JSON 文件中加载数据
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        item["Language Query"] = capitalize_and_clean(item["Language Query"])

    # 提取所有唯一的 Language Query
    unique_queries = list({item["Language Query"] for item in data})

    # 格式化为目标结构
    output = {"unique query": unique_queries}

    # 保存修改后的输入数据和唯一查询到文件
    with open(input_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    # 保存为 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)

    print(f"Unique queries have been saved to {output_file}.")

    with open(output_file, "r", encoding="utf-8") as f:
        unique_data = json.load(f)

    for query in unique_data["unique query"]:
        if query and not query[0].isupper():
            print(f"The following query does not start with an uppercase letter: {query}")

# get_unique_queries("../../data/Ours/OVIS-training.json", "unique_queries_ovis-training.json")
# get_unique_queries("../../data/Ours/OVIS-valid.json", "unique_queries_ovis-valid.json")
# get_unique_queries("../../data/Ours/MOT17-training.json", "unique_queries_mot17-training.json")
# get_unique_queries("../../data/Ours/MOT17-valid.json", "unique_queries_mot17-valid.json")
# get_unique_queries("../../data/Ours/MOT20-training.json", "unique_queries_mot20-training.json")
# get_unique_queries("../../data/Ours/MOT20-valid.json", "unique_queries_mot20-valid.json")

def unify_txt(file_path):
    with open(file_path, 'r') as infile:
        lines = infile.readlines()

    # 处理每一行
    processed_lines = [capitalize_and_clean(line.strip()) for line in lines]

    # 将处理后的内容写入新的txt文件
    with open(file_path, 'w') as outfile:
        for line in processed_lines:
            outfile.write(line + '\n')

# unify_txt('../../data/Ours/OVIS-training_unique_language_queries.txt')
# unify_txt('../../data/Ours/OVIS-valid_unique_language_queries.txt')
# unify_txt('../../data/Ours/MOT20-training_unique_language_queries.txt')
# unify_txt('../../data/Ours/MOT20-valid_unique_language_queries.txt')
# unify_txt('../../data/Ours/MOT17-training_unique_language_queries.txt')
# unify_txt('../../data/Ours/MOT17-valid_unique_language_queries.txt')
#
# unify_txt('../../data/Ours/OVIS-training_unique_language_queries_rephrased.txt')
# unify_txt('../../data/Ours/OVIS-valid_unique_language_queries_rephrased.txt')
# unify_txt('../../data/Ours/MOT20-training_unique_language_queries_rephrased.txt')
# unify_txt('../../data/Ours/MOT20-valid_unique_language_queries_rephrased.txt')
# unify_txt('../../data/Ours/MOT17-training_unique_language_queries_rephrased.txt')
# unify_txt('../../data/Ours/MOT17-valid_unique_language_queries_rephrased.txt')

def unify_json(file_path):
    with open(file_path, 'r') as infile:
        data = json.load(infile)

    # 处理每一条数据
    for item in data:
        # 处理 'rephrased_content' 和 'original_content'
        item['rephrased_content'] = capitalize_and_clean(item['rephrased_content'])
        item['original_content'] = capitalize_and_clean(item['original_content'])

        # 处理 'extra_rephrased' 列表中的每个句子
        if 'extra_rephrased' in item:
            item['extra_rephrased'] = [capitalize_and_clean(sentence) for sentence in item['extra_rephrased']]

    # 直接覆盖原文件
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, indent=4)


unify_json('../../data/Ours/MOT17-training_combined_language_queries.json')
unify_json('../../data/Ours/MOT17-valid_combined_language_queries.json')
unify_json('../../data/Ours/MOT20-training_combined_language_queries.json')
unify_json('../../data/Ours/MOT20-valid_combined_language_queries.json')
unify_json('../../data/Ours/OVIS-training_combined_language_queries.json')
unify_json('../../data/Ours/OVIS-valid_combined_language_queries.json')
