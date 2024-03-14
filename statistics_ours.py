import csv
import json
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")


def csv_to_json(csv_file_path, json_file_path):
    csv_data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    with open(json_file_path, 'w') as json_file:
        json.dump(csv_data, json_file, indent=2)


def generate_all_jsons():
    csv_to_json('data/Ours/Grounded Tracking Annotations - MOT17(Ashiq).csv',
                'data/generated_by_code/ours_json/gta_mot17_ashiq.json')
    csv_to_json('data/Ours/Grounded Tracking Annotations - MOT17(Seenat).csv',
                'data/generated_by_code/ours_json/gta_mot17_seenat.json')
    csv_to_json('data/Ours/Grounded Tracking Annotations - MOT17-Test(Ashiq).csv',
                'data/generated_by_code/ours_json/gta_mot17_test_ashiq.json')
    csv_to_json('data/Ours/Grounded Tracking Annotations - MOT17-Test(Seenat).csv',
                'data/generated_by_code/ours_json/gta_mot17_test_seenat.json')


# generate_all_jsons()
paths = ['data/generated_by_code/ours_json/gta_mot17_ashiq.json',
         'data/generated_by_code/ours_json/gta_mot17_seenat.json',
         'data/generated_by_code/ours_json/gta_mot17_test_ashiq.json',
         'data/generated_by_code/ours_json/gta_mot17_test_seenat.json']


def get_all_queries(file_paths):
    unique_queries = set()
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                unique_queries.add(item['Language Query'])
    return unique_queries


unique_queries = get_all_queries(paths)
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
    print(f'The number of different verbs (include tense): {len(item_frequency)}')  #

    sorted_items = sorted(item_frequency.items(), key=lambda x: x[1], reverse=True)

    data_dict = {}

    for item, frequency in sorted_items:
        print(f'{item}: {frequency}')
        data_dict[item] = frequency

    output_file_path = 'data/generated_by_code/verbs_json/verbs_ours.json'

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)


get_verb_and_frequency_from_sentences(unique_queries)


