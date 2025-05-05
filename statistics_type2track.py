import json
import spacy
from collections import Counter

unique_captions = set()

def calculate_caption(unique_set, file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    annotations = data.get("annotations", [])

    for annotation in annotations:
        captions = annotation.get("captions", [])

        for caption in captions:
            if caption is not None:
                unique_set.add(caption)


file_path1 = 'data/Type-to-Track/annotations/v1.0/mot17_train_coco.json'
file_path2 = 'data/Type-to-Track/annotations/v1.0/mot17_test_coco.json'
file_path3 = 'data/Type-to-Track/annotations/v1.0/tao_train_coco.json'

calculate_caption(unique_captions, file_path1)
calculate_caption(unique_captions, file_path2)
calculate_caption(unique_captions, file_path3)
# 3567
# print(f'There are {len(unique_captions)} different kinds of captions')

nlp = spacy.load("en_core_web_sm")


# note: some verbs are not really verbs!
def get_verb_and_frequency_from_sentences(sentences):
    verbs_list = []

    for sentence in sentences:
        doc = nlp(sentence)
        # type of verbs is <list>
        verbs = [token for token in doc if token.pos_ == "VERB"]
        ignore_verbs = ['hand']
        if any(verb.text in ignore_verbs for verb in verbs):
            verbs = [verb for verb in verbs if verb.text not in ignore_verbs]
        # print(verbs)
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


    # count frequency of the words
    item_frequency = Counter(verbs_list)
    print(f'The number of different verbs (include tense): {len(item_frequency)}')  # 197

    sorted_items = sorted(item_frequency.items(), key=lambda x: (-x[1], x[0]))
    data_dict = {}

    for item, frequency in sorted_items:
        # print(f'{item}: {frequency}')
        data_dict[item] = frequency

    output_file_path = 'data/generated_by_code/verbs_json/verbs_type2track.json'

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)


get_verb_and_frequency_from_sentences(unique_captions)




