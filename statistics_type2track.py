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
print(f'There are {len(unique_captions)} different kinds of captions')
calculate_caption(unique_captions, file_path2)
print(f'There are {len(unique_captions)} different kinds of captions')
calculate_caption(unique_captions, file_path3)
print(f'There are {len(unique_captions)} different kinds of captions')

# individual calculation, maybe there are some duplicates between mot17_train_coco and mot17_train_coco
# 2582 tao_train_coco.json
# 427 mot17_train_coco.json
# 828 mot17_train_coco.json
# print(f'There are {len(unique_captions)} different kinds of captions')
#
# for unique_caption in unique_captions:
#     print(unique_caption)

nlp = spacy.load("en_core_web_sm")


# note: some verbs are not really verbs!
def get_verb_and_frequency_from_sentences(sentences):
    verbs_list = []

    for sentence in sentences:
        doc = nlp(sentence)
        # type of verbs is <list>
        verbs = [token.text for token in doc if token.pos_ == 'VERB']
        # print(verbs)
        verbs_list.extend(verbs)
        # if 'hand' in verbs:
        #     print(sentence)
    # print(f'Verbs: {verbs_list}')

    # count frequency of the words
    item_frequency = Counter(verbs_list)
    print(f'The number of different verbs (include tense): {len(item_frequency)}')  # 199

    sorted_items = sorted(item_frequency.items(), key=lambda x: x[1], reverse=True)
    data_dict = {}

    for item, frequency in sorted_items:
        print(f'{item}: {frequency}')
        data_dict[item] = frequency

    output_file_path = 'data/generated_by_code/verbs_json/verbs_type2track.json'

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)


get_verb_and_frequency_from_sentences(unique_captions)




