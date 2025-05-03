# #Tracks means the Number of unique object id from each video
import json
import spacy
from collections import Counter

file_paths = ['data/VidSTG/annotations/test_annotations.json', 'data/VidSTG/annotations/train_annotations.json',
              'data/VidSTG/annotations/val_annotations.json']
total_track_count = 0
unique_captions_set = set()
nlp = spacy.load("en_core_web_sm")


def count_subject_objects(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    vid_count = {}

    for entry in data:
        vid = entry.get('vid')
        subjects_objects = entry.get('subject/objects', [])

        if vid is None or vid in vid_count:
            continue

        vid_count[vid] = len(subjects_objects)

    return vid_count


'''
return: caption_count
Get all captions description of every videos.
An example: 5379879696: {'an adult in black is above a ski on the snow.', 'an adult rides a ski on the snow.'}
'''
def calculate_captions(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    caption_count = {}
    captions_description_count = 0  # Total description count: 6770

    for entry in data:
        vid = entry.get('vid')
        captions = entry.get('captions', [])
        captions_description = set([caption['description'] for caption in captions])

        # for description in descriptions:
        #     print(description)
        if vid is not None:
            if vid in caption_count:
                caption_count[vid].update(captions_description)
            else:
                caption_count[vid] = captions_description

        captions_description_count += len(captions_description)
    return caption_count


def get_unique_captions(caption_count):
    for descriptions_set in caption_count.values():
        unique_captions_set.update(descriptions_set)
    return unique_captions_set


def get_verb_and_frequency_from_sentences(sentences):
    # take a long time to finish computing
    verbs_list = []

    for sentence in sentences:
        doc = nlp(sentence)
        # type of verbs is <list>
        verbs = [token for token in doc if token.pos_ == "VERB" and token.dep_ != "AUX"]
        ignore_verbs = ['hand']
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

        if 'hand' in filtered_verbs:
            print(sentence)

        verbs_list.extend(filtered_verbs)

    # count frequency of the words
    item_frequency = Counter(verbs_list)
    print(f'The number of different verbs (include tense): {len(item_frequency)}')  # 246

    sorted_items = sorted(item_frequency.items(), key=lambda x: (-x[1], x[0]))
    data_dict = {}

    for item, frequency in sorted_items:
        # print(f'{item}: {frequency}')
        data_dict[item] = frequency

    output_file_path = 'data/generated_by_code/verbs_json/verbs_stvg.json'

    with open(output_file_path, 'w') as f:
        json.dump(data_dict, f, indent=4)

    print("Data saved to:", output_file_path)


total_description_count = 0

for path in file_paths:
    vid_counts = count_subject_objects(path)
    # print('len: ', len(vid_counts))
    for vid, count in vid_counts.items():
        # print(f'vid: {vid}, subject/objects count: {count}')
        total_track_count += count

    captions_description = calculate_captions(path)

    # Length of unique_captions_set is 29509 != 44808
    unique_captions_set.update(get_unique_captions(captions_description))

    # for vid, descriptions in captions_description.items():
    #     print(f"{vid}: {descriptions}")

print(len(unique_captions_set)) # 29509
print(f'Total subject/objects count: {total_track_count}')  # 35044
get_verb_and_frequency_from_sentences(unique_captions_set)

# print(f'Total description count: {total_description_count}')

# video 732+5436+602 = 6770 != 6924
# test 3683 train 28275 val 3086  =  35044

count_sum = 0
for path in file_paths:
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    count = len(data)
    count_sum += count
    # test_annotations: 4610, train_annotations: 36202, val_annotations: 3996
    print(f"{path}里JSON数组对象的数量: {count}")
print(count_sum) # 44808
