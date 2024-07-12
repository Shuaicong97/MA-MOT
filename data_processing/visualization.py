import json
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# TODO: need to add MOT20 later
verbs_mot17_ovis = '../data/generated_by_code/verbs_json/verbs_mot17_ovis.json'
verbs_mot17 = '../data/generated_by_code/verbs_json/verbs_mot17.json'
verbs_ovis = '../data/generated_by_code/verbs_json/verbs_ovis.json'


def draw_wordcloud(input_path, output_path):
    with open(input_path, 'r') as f:
        data = json.load(f)

    font_path = '/Library/Fonts/Arial.ttf'
    wordcloud = WordCloud(width=1600, height=800, background_color='white', font_path=font_path,
                          scale=2).generate_from_frequencies(data)

    plt.figure(figsize=(20, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    # output_path = '../data/Ours/Visualization/wordcloud-mot17-ovis.png'
    plt.savefig(output_path, format='png', dpi=300)
    # plt.show()


draw_wordcloud(verbs_mot17_ovis, '../data/Ours/Visualization/wordcloud-mot17-ovis.png')
draw_wordcloud(verbs_mot17, '../data/Ours/Visualization/wordcloud-mot17.png')
draw_wordcloud(verbs_ovis, '../data/Ours/Visualization/wordcloud-ovis.png')
