import json
import spacy
from collections import Counter

nlp = spacy.load("en_core_web_sm")

with open('data/HC-STVG/v1/HCVG_query.json', 'r') as file:
    data_dict = json.load(file)

values_list = list(data_dict.values())
unique_values_set = set(values_list)

line_count = len(data_dict.values())

print(f'The number of values in the JSON file is: {len(unique_values_set)}')  # 4378


def get_verb_and_frequency_from_sentences(sentences):
    # take a long time to finish computing
    verbs_list = []

    for sentence in sentences:
        doc = nlp(sentence)
        # type of verbs is <list>
        verbs = [token.text for token in doc if token.pos_ == 'VERB']
        verbs_list.extend(verbs)
        # if 'hand' in verbs:
        #     print(sentence)

    # count frequency of the words
    item_frequency = Counter(verbs_list)
    print(f'The number of different verbs (include tense): {len(item_frequency)}')  # 520

    sorted_items = sorted(item_frequency.items(), key=lambda x: x[1], reverse=True)
    data_dict = {}

    for item, frequency in sorted_items:
        print(f'{item}: {frequency}')
        data_dict[item] = frequency

    output_file_path = 'data/verbs_json/verbs_hc-stvg.json'

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)


get_verb_and_frequency_from_sentences(unique_values_set)
