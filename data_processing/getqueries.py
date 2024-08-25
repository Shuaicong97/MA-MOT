import csv

# 设置CSV文件路径
mot17_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.csv'
mot17_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.csv'
mot20_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training.csv'
mot20_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid.csv'
ovis_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training.csv'
ovis_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid.csv'

output_txt_mot17_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training_unique_language_queries.txt'
output_txt_mot17_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid_unique_language_queries.txt'
output_txt_mot20_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training_unique_language_queries.txt'
output_txt_mot20_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid_unique_language_queries.txt'
output_txt_ovis_training = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training_unique_language_queries.txt'
output_txt_ovis_valid = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid_unique_language_queries.txt'


def get_unique_queries(csv_file_path, output_txt_file_path):
    # 创建一个集合来存储不重复的Language Query
    unique_queries = set()

    # 读取CSV文件
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            language_query = row['Language Query']
            unique_queries.add(language_query)

    # 将不重复的Language Query写入txt文件
    with open(output_txt_file_path, mode='w', encoding='utf-8') as file:
        for query in sorted(unique_queries):
            file.write(query + '\n')

    print(f"共提取了 {len(unique_queries)} 个不重复的Language Query，并已保存到 {output_txt_file_path} 中。")


get_unique_queries(mot17_training, output_txt_mot17_training)
get_unique_queries(mot17_valid, output_txt_mot17_valid)
get_unique_queries(mot20_training, output_txt_mot20_training)
get_unique_queries(mot20_valid, output_txt_mot20_valid)
get_unique_queries(ovis_training, output_txt_ovis_training)
get_unique_queries(ovis_valid, output_txt_ovis_valid)

