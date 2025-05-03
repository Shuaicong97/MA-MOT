import json
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")
'''
The number of entries in the valid JSON file is: 507
The number of entries in the test JSON file is: 305
The number of entries in the train JSON file is: 3471
'''

def process_json_file(file_path, video_expression_dict):
    with open(file_path, 'r') as file:
        data_dict = json.load(file)

    for video_id, video_data in data_dict.get('videos', {}).items():
        expressions = video_data.get('expressions', {})

        if video_id not in video_expression_dict:
            video_expression_dict[video_id] = set()

        for expression_id, expression_data in expressions.items():
            expression = expression_data.get('exp', '')
            video_expression_dict[video_id].add(expression)

    return video_expression_dict


# test和valid中有部分video重复 => video_expression_dict的长度就是视频的数量
video_expression_dict = {}
video_expression_dict = process_json_file('data/Ref-YT/meta_expressions/test/meta_expressions.json', video_expression_dict)
video_expression_dict = process_json_file('data/Ref-YT/meta_expressions/train/meta_expressions.json', video_expression_dict)
video_expression_dict = process_json_file('data/Ref-YT/meta_expressions/valid/meta_expressions.json', video_expression_dict)
print(f"Total length of expression_dict: {len(video_expression_dict)}")  # 3978

unique_expression_set = set()
expression_list = []
for video_id, expressions in video_expression_dict.items():
    for expression in expressions:
        unique_expression_set.update([expression])
        expression_list.append(expression)

print(f"Expressions: {len(unique_expression_set)}")  # 14289
# #Queries
print(f"Expressions list: {len(expression_list)}")  # 14952

# expression_counter = Counter(expression_list)
# # 找出出现多于一次的表达式
# duplicates = [exp for exp, count in expression_counter.items() if count > 1]
# e.g.
# - a dead deer (count: 2)
# - a cheetah eating (count: 2)
# - a giant panda playing (count: 2)
# - a panda playing (count: 4)
# - a yellow umbrella (count: 2)
# print(f"Number of duplicate expressions: {len(duplicates)}")
# print("Some duplicated expressions:")
# for exp in duplicates[:10]:  # 打印前10个重复表达式作为样例
#     print(f"- {exp} (count: {expression_counter[exp]})")

# Both functions work for calculating the number of queries!
paths = ['data/Ref-YT/meta_expressions/test/meta_expressions.json',
         'data/Ref-YT/meta_expressions/train/meta_expressions.json',
         'data/Ref-YT/meta_expressions/valid/meta_expressions.json']


def get_all_expressions(file_paths):
    unique_queries_set = set()
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)

        for video_id, video_data in data.get('videos', {}).items():
            expressions = video_data.get('expressions', {})
            for expression_id, expression_data in expressions.items():
                expression = expression_data.get('exp', '')
                unique_queries_set.add(expression)
    return unique_queries_set


unique_queries = get_all_expressions(paths)
print(f'There are in total {len(unique_queries)} different kinds of queries.')  # 634  14289

def get_verb_and_frequency_from_sentences(sentences):
    # take a long time to finish computing
    verbs_list = []

    for sentence in sentences:
        doc = nlp(sentence)
        # type of verbs is <list>
        verbs = [token for token in doc if token.pos_ == "VERB" and token.dep_ != "AUX"]
        ignore_verbs = ['j57']
        if any(verb.text in ignore_verbs for verb in verbs):
            verbs = [verb for verb in verbs if verb.text not in ignore_verbs]

        filtered_verbs = []
        for i, cur_verb in enumerate(verbs):
            cur_verb_index = cur_verb.i

            # 查找 cur_verb 前一个单词
            if cur_verb_index > 0:
                pre_verb = doc[cur_verb_index - 1]

                # 如果 pre_verb 是动词并且在 verbs 中，说明是连续动词，应该跳过当前动词
                if pre_verb.pos_ == "VERB" and pre_verb in verbs:
                    continue  # 跳过当前动词

            # 如果没有移除，则保留当前动词
            filtered_verbs.append(cur_verb.text)

        verbs_list.extend(filtered_verbs)

    # count frequency of the words
    item_frequency = Counter(verbs_list)
    print(f'The number of different verbs (include tense): {len(item_frequency)}')  # 878

    sorted_items = sorted(item_frequency.items(), key=lambda x: (-x[1], x[0]))

    data_dict = {}

    for item, frequency in sorted_items:
        # print(f'{item}: {frequency}')
        data_dict[item] = frequency

    output_file_path = 'data/generated_by_code/verbs_json/verbs_refer-yt.json'

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)

get_verb_and_frequency_from_sentences(unique_expression_set)
