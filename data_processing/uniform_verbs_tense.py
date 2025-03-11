import json
import nltk
nltk.download('averaged_perceptron_tagger_eng')
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

from nltk import word_tokenize, pos_tag

# Sample sentence
sentence = 'She starts running in the park.'

# Tokenize the sentence
tokens = word_tokenize(sentence)

# Perform POS tagging
pos_tags = pos_tag(tokens)

# POS Tags:  [('She', 'PRP'), ('starts', 'VBZ'), ('running', 'VBG'), ('in', 'IN'), ('the', 'DT'), ('park', 'NN'), ('.', '.')]
# Detected Verbs: ['starts', 'running']
# Display the POS tags
print("POS Tags: ", pos_tags)
verbs = [word for word, tag in pos_tags if tag.startswith('VB')]
print("Detected Verbs:", verbs)

def convert_verbs_to_base(json_file, output_file, output_path):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    lemmatizer = WordNetLemmatizer()
    base_verbs = {}

    for word, freq in data.items():
        base_form = lemmatizer.lemmatize(word, wordnet.VERB)  # 转换为原形
        if base_form in base_verbs:
            base_verbs[base_form] += freq  # 归一化后合并计数
        else:
            base_verbs[base_form] = freq

    # 按频率降序排序
    sorted_base_verbs = dict(sorted(base_verbs.items(), key=lambda item: item[1], reverse=True))

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sorted_base_verbs, f, ensure_ascii=False, indent=4)

    print(f"转换完成，结果已保存到 {output_file}")
    print(f"输出 JSON 长度: {len(sorted_base_verbs)}")  # 478

    # 绘制前 50 个结果的柱状图
    top_50 = list(sorted_base_verbs.items())[:50]
    words, freqs = zip(*top_50)

    plt.figure(figsize=(15, 6))
    plt.bar(words, freqs, color='skyblue')
    # plt.xlabel("Verbs")
    plt.ylabel("Count")
    plt.title("Actions")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_path, format='png', dpi=300)

    # plt.show()


convert_verbs_to_base('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/verbs_json/verbs/verbs_ours_all.json',
                      'verbs_output.json', '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Visualization/top50_verbs-.png')
