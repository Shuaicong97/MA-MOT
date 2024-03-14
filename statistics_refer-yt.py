import json
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")
'''
The number of entries in the valid JSON file is: 507
The number of entries in the test JSON file is: 305
The number of entries in the train JSON file is: 3471
'''

unique_expression_set = set()


def process_json_file(file_path, video_expression_dict):
    with open(file_path, 'r') as file:
        data_dict = json.load(file)

    for video_id, video_data in data_dict.get('videos', {}).items():
        expressions = video_data.get('expressions', {})
        frames = video_data.get('frames', [])

        if video_id not in video_expression_dict:
            video_expression_dict[video_id] = set()

        for expression_id, expression_data in expressions.items():
            expression = expression_data.get('exp', '')
            video_expression_dict[video_id].add(expression)

    return video_expression_dict


video_expression_dict = {}

video_expression_dict = process_json_file('data/Ref-YT/meta_expressions/test/meta_expressions.json',
                                          video_expression_dict)
video_expression_dict = process_json_file('data/Ref-YT/meta_expressions/train/meta_expressions.json',
                                          video_expression_dict)
video_expression_dict = process_json_file('data/Ref-YT/meta_expressions/valid/meta_expressions.json',
                                          video_expression_dict)
print(f"Total length of expression_dict: {len(video_expression_dict)}")  # 3978

for video_id, expressions in video_expression_dict.items():
    # print(f"Video ID: {video_id}")
    # print("Expressions:")
    for expression in expressions:
        # print(f"- {expression}")
        unique_expression_set.update([expression])

print(f"Expressions: {len(unique_expression_set)}")  # 14289

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
print(f'There are in total {len(unique_queries)} different kinds of queries.')  # 634


def get_verb_and_frequency_from_sentences(sentences):
    # take a long time to finish computing
    verbs_list = []

    for sentence in sentences:
        doc = nlp(sentence)
        # type of verbs is <list>
        verbs = [token.text for token in doc if token.pos_ == 'VERB']
        verbs_list.extend(verbs)
        # if 'j57' in verbs:
        #     print(sentence)

    # count frequency of the words
    item_frequency = Counter(verbs_list)
    print(f'The number of different verbs (include tense): {len(item_frequency)}')  # 882

    sorted_items = sorted(item_frequency.items(), key=lambda x: x[1], reverse=True)

    data_dict = {}

    for item, frequency in sorted_items:
        print(f'{item}: {frequency}')
        data_dict[item] = frequency

    output_file_path = 'data/generated_by_code/verbs_json/verbs_refer-yt.json'

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)

# get_verb_and_frequency_from_sentences(unique_expression_set)
