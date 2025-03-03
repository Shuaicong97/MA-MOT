import csv
import json
import spacy
from collections import Counter
import matplotlib.pyplot as plt

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

mot17_training_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/rephrased_annotations/MOT17-training-doubled.json'
mot17_valid_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/rephrased_annotations/MOT17-valid-doubled.json'
mot20_training_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/rephrased_annotations/MOT20-training-doubled.json'
mot20_valid_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/rephrased_annotations/MOT20-valid-doubled.json'
ovis_training_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/rephrased_annotations/OVIS-training-doubled.json'
ovis_valid_rephrased = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/rephrase_queries/rephrased_annotations/OVIS-valid-doubled.json'

paths_all = [mot17_training_rephrased, mot17_valid_rephrased, mot20_training_rephrased, mot20_valid_rephrased, ovis_training_rephrased, ovis_valid_rephrased]

paths_mot17 = [mot17_training_rephrased, mot17_valid_rephrased]
paths_mot20 = [mot20_training_rephrased, mot20_valid_rephrased]
paths_ovis = [ovis_training_rephrased, ovis_valid_rephrased]

mot17_training_original = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.json'
mot17_valid_original = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.json'
mot20_training_original = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training.json'
mot20_valid_original = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid.json'
ovis_training_original = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training.json'
ovis_valid_original = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid.json'

paths_all_original = [mot17_training_original, mot17_valid_original, mot20_training_original, mot20_valid_original, ovis_training_original, ovis_valid_original]
paths_mot17_original = [mot17_training_original, mot17_valid_original]
paths_mot20_original = [mot20_training_original, mot20_valid_original]
paths_ovis_original = [ovis_training_original, ovis_valid_original]


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

print(f'There are in total {len(unique_queries_all)} different kinds of queries.')  # 7838
print(f'There are in total {len(unique_queries_mot17)} different kinds of queries in mot17.')  # 1255
print(f'There are in total {len(unique_queries_ovis)} different kinds of queries in ovis.')  # 5474
print(f'There are in total {len(unique_queries_mot20)} different kinds of queries in mot20.')  # 1127


def get_word_count_distribution(unique_queries, output_path):
    word_count_distribution = {}

    # Count word frequencies in the queries
    for query in unique_queries:
        word_count = len(query.split())
        if word_count in word_count_distribution:
            word_count_distribution[word_count] += 1
        else:
            word_count_distribution[word_count] = 1

    # Plotting the distribution
    x = list(word_count_distribution.keys())  # Word counts (x-axis)
    y = list(word_count_distribution.values())  # Query counts (y-axis)

    plt.figure(figsize=(10, 6))
    plt.bar(x, y)
    plt.xlabel('Word Count per Query')
    plt.ylabel('Count of Queries')
    plt.title('Distribution of Query Word Count')
    plt.xticks(x)  # Ensure each word count has its own tick on the x-axis

    plt.savefig(output_path, format='png', dpi=300)
    print(f"结果已保存到 {output_path}")



get_word_count_distribution(unique_queries_all, '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Visualization/word_count_distribution_all.png')



def get_number_of_entries(file_paths):
    total_entries = 0
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        item_count = len(json_data)
        total_entries += item_count

    print(f"The number of items in all three datasets is: {total_entries}")


get_number_of_entries(paths_all)
get_number_of_entries(paths_mot17)
get_number_of_entries(paths_ovis)
get_number_of_entries(paths_mot20)

# print()
#
# get_number_of_entries(paths_all_original)
# get_number_of_entries(paths_mot17_original)
# get_number_of_entries(paths_ovis_original)
# get_number_of_entries(paths_mot20_original)

def get_verb_and_frequency_from_sentences(dataset, sentences, output_file_path):
    # take a long time to finish computing
    verbs_list = []

    for sentence in sentences:
        doc = nlp(sentence)
        # type of verbs is <list>
        verbs = [token.text for token in doc if token.pos_ == 'VERB']
        if len(verbs) == 1 and verbs[0] in ('left', 'rightward'):
            # print(f"跳过的句子: {sentence}")
            continue
        verbs_list.extend(verbs)


    # count frequency of the words
    item_frequency = Counter(verbs_list)
    print(f'The number of different verbs (include tense) in {dataset}: {len(item_frequency)}')

    sorted_items = sorted(item_frequency.items(), key=lambda x: (-x[1], x[0]))

    data_dict = {}

    for item, frequency in sorted_items:
        data_dict[item] = frequency

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)


get_verb_and_frequency_from_sentences('all', unique_queries_all, 'data/generated_by_code/verbs_json/verbs/verbs_ours_all.json')
get_verb_and_frequency_from_sentences('mot17', unique_queries_mot17, 'data/generated_by_code/verbs_json/verbs/verbs_mot17.json')
get_verb_and_frequency_from_sentences('ovis', unique_queries_ovis, 'data/generated_by_code/verbs_json/verbs/verbs_ovis.json')
get_verb_and_frequency_from_sentences('mot20', unique_queries_mot20, 'data/generated_by_code/verbs_json/verbs/verbs_mot20.json')


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

# There are in total 7863 different kinds of queries.
# There are in total 1255 different kinds of queries in mot17.
# There are in total 5499 different kinds of queries in ovis.
# There are in total 1127 different kinds of queries in mot20.
# The number of items in all three datasets is: 19563
# The number of different verbs (include tense) in all: 878
# Data saved to: data/generated_by_code/verbs_json/verbs/verbs_ours_all.json
# The number of different verbs (include tense) in mot17: 263
# Data saved to: data/generated_by_code/verbs_json/verbs/verbs_mot17.json
# The number of different verbs (include tense) in ovis: 741
# Data saved to: data/generated_by_code/verbs_json/verbs/verbs_ovis.json
# The number of different verbs (include tense) in mot20: 219
# Data saved to: data/generated_by_code/verbs_json/verbs/verbs_mot20.json