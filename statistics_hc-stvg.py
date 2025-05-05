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
        verbs = [token for token in doc if token.pos_ == "VERB"]
        ignore_verbs = ['hand']
        if any(verb.text in ignore_verbs for verb in verbs):
            verbs = [verb for verb in verbs if verb.text not in ignore_verbs]
        filtered_verbs = []
        for i, cur_verb in enumerate(verbs):
            cur_verb_index = cur_verb.i

            # 查找 cur_verb 前一个单词
            if cur_verb_index > 0:
                pre_verb = doc[cur_verb_index - 1]

                # 如果 pre_verb 是动词并且在 verbs 中，说明是连续动词，应该移除前面的动词
                if pre_verb.pos_ == "VERB" and pre_verb in verbs:
                    filtered_verbs.remove(pre_verb.text)

            # 如果没有移除，则保留当前动词
            filtered_verbs.append(cur_verb.text)
        if 'hand' in filtered_verbs:
            print(sentence)

        verbs_list.extend(filtered_verbs)
        # if 'hand' in verbs:
        #     print(sentence)

    # count frequency of the words
    item_frequency = Counter(verbs_list)
    print(f'The number of different verbs (include tense): {len(item_frequency)}')  # 515

    sorted_items = sorted(item_frequency.items(), key=lambda x: (-x[1], x[0]))
    data_dict = {}

    for item, frequency in sorted_items:
        data_dict[item] = frequency

    output_file_path = 'data/generated_by_code/verbs_json/verbs_hc-stvg.json'

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)


get_verb_and_frequency_from_sentences(unique_values_set)
