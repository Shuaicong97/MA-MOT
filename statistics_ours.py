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
# paths = ['data/generated_by_code/ours_json/gta_mot17_ashiq.json',
#          'data/generated_by_code/ours_json/gta_mot17_seenat.json',
#          'data/generated_by_code/ours_json/gta_mot17_test_ashiq.json',
#          'data/generated_by_code/ours_json/gta_mot17_test_seenat.json']

paths_all = ['data/Ours/MOT17-training-doubled-3.json', 'data/Ours/MOT17-valid-doubled-3.json',
             'data/Ours/OVIS-training-doubled-3.json', 'data/Ours/OVIS-valid-doubled-3.json',
             'data/Ours/MOT20-training-doubled-3.json', 'data/Ours/MOT20-valid-doubled-3.json']

paths_mot17 = ['data/Ours/MOT17-training-doubled-3.json', 'data/Ours/MOT17-valid-doubled-3.json']
paths_ovis = ['data/Ours/OVIS-training-doubled-3.json', 'data/Ours/OVIS-valid-doubled-3.json']
paths_mot20 = ['data/Ours/MOT20-training-doubled-3.json', 'data/Ours/MOT20-valid-doubled-3.json']


def get_all_queries(file_paths):
    unique_queries = set()
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                unique_queries.add(item['Language Query'])
    return unique_queries


unique_queries_all = get_all_queries(paths_all)
unique_queries_mot17 = get_all_queries(paths_mot17)
unique_queries_ovis = get_all_queries(paths_ovis)
unique_queries_mot20 = get_all_queries(paths_mot20)

print(f'There are in total {len(unique_queries_all)} different kinds of queries.')  # 3963
print(f'There are in total {len(unique_queries_mot17)} different kinds of queries in mot17.')  # 634
print(f'There are in total {len(unique_queries_ovis)} different kinds of queries in ovis.')  # 2760
print(f'There are in total {len(unique_queries_mot20)} different kinds of queries in mot20.')  # 581


def get_number_of_entries(file_paths):
    total_entries = 0
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        item_count = len(json_data)
        total_entries += item_count

    print(f"The number of items in all three datasets is: {total_entries}")  # 9779


get_number_of_entries(paths_all)


def get_verb_and_frequency_from_sentences(dataset, sentences, output_file_path):
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
    # all: 486, mot17: 150, ovis: 388, mot20: 117
    # all: 876, mot17: 260, ovis: 739, mot20: 219 (use -3.json)
    print(f'The number of different verbs (include tense) in {dataset}: {len(item_frequency)}')

    sorted_items = sorted(item_frequency.items(), key=lambda x: (-x[1], x[0]))

    data_dict = {}

    for item, frequency in sorted_items:
        data_dict[item] = frequency

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)


get_verb_and_frequency_from_sentences('all', unique_queries_all, 'data/generated_by_code/verbs_json/verbs_ours_all.json')
get_verb_and_frequency_from_sentences('mot17', unique_queries_mot17, 'data/generated_by_code/verbs_json/verbs_mot17.json')
get_verb_and_frequency_from_sentences('ovis', unique_queries_ovis, 'data/generated_by_code/verbs_json/verbs_ovis.json')
get_verb_and_frequency_from_sentences('mot20', unique_queries_mot20, 'data/generated_by_code/verbs_json/verbs_mot20.json')


def get_subject_frequency_from_sentences(sentences, output_file_path):
    subjects = []

    for sentence in sentences:
        doc = nlp(sentence)
        for token in doc:
            if token.dep_ == "nsubj":
                subjects.append(token.text)

    subject_freq = Counter(subjects)
    print(subject_freq)


# get_subject_frequency_from_sentences(unique_queries_ovis, 'data/generated_by_code/subs_json/subs_ovis.json')

