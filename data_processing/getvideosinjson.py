# First step: get train and valid videos
import pandas as pd
import json
import csv
import os


# OVIS -----
a = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS(Seenat).csv'
b = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/Clean OVIS(Seenat).csv'
b2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/OVIS(Seenat).csv'
c = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS(Ashiq).csv'
d = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/Clean OVIS(Ashiq).csv'
d2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/OVIS(Ashiq).csv'
e = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS-Test(Seenat).csv'
f = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/Clean OVIS-Test(Seenat).csv'
f2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/OVIS-Test(Seenat).csv'
g = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS-Test(Ashiq).csv'
h = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/Clean OVIS-Test(Ashiq).csv'
h2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/OVIS-Test(Ashiq).csv'

# MOT17 -----
a1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT17(Ashiq).csv'
b1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/Clean MOT17(Ashiq).csv'
b3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT17(Ashiq).csv'
c1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT17(Seenat).csv'
d1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/Clean MOT17(Seenat).csv'
d3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT17(Seenat).csv'
e1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT17-Test(Ashiq).csv'
f1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/Clean MOT17-Test(Ashiq).csv'
f3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT17-Test(Ashiq).csv'
g1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT17-Test(Seenat).csv'
h1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/Clean MOT17-Test(Seenat).csv'
h3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT17-Test(Seenat).csv'

# MOT20 -----
m1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT20(Ashiq).csv'
m2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/Clean MOT20(Ashiq).csv'
m3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT20(Ashiq).csv'
n1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT20(Seenat).csv'
n2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/Clean MOT20(Seenat).csv'
n3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT20(Seenat).csv'


def reformat_csv_file(file_path, output_file_path):
    df = pd.read_csv(file_path)
    # remove all columns where the name is blank
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # reformat value type to int
    int_columns = ['ID mark frame', 'QID', 'IDs', 'Start', 'End', 'Query ID', 'Start Frame', 'End Frame']
    for column in int_columns:
        if column in df.columns:
            df[column] = df[column].astype(pd.Int64Dtype())
    df['Language Query'] = df['Language Query'].str.strip()

    df.to_csv(output_file_path, index=False)


# only need to be done once at the first
# reformat_csv_file(a, b)
# reformat_csv_file(c, d)
# reformat_csv_file(e, f)
# reformat_csv_file(g, h)
# reformat_csv_file(a1, b1)
# reformat_csv_file(c1, d1)
# reformat_csv_file(e1, f1)
# reformat_csv_file(g1, h1)
reformat_csv_file(m1, m2)
reformat_csv_file(n1, n2)


def remove_invalid_rows(data_type, input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
            open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in reader:
            if data_type == 'mot17' and row['Track ID'] and row['Start Frame'] and row['End Frame']:
                writer.writerow(row)
            if data_type == 'ovis' or data_type == 'mot20' and row['IDs'] and row['Start'] and row['End']:
                writer.writerow(row)

    # print(f"Filtered data has been saved to {output_file}")


# remove_invalid_rows('ovis', b, b2)
# remove_invalid_rows('ovis', d, d2)
# remove_invalid_rows('ovis', f, f2)
# remove_invalid_rows('ovis', h, h2)
# remove_invalid_rows('mot17', b1, b3)
# remove_invalid_rows('mot17', d1, d3)
# remove_invalid_rows('mot17', f1, f3)
# remove_invalid_rows('mot17', h1, h3)
remove_invalid_rows('mot20', m2, m3)
remove_invalid_rows('mot20', n2, n3)


def merge_csv_files(a_file, b_file, output_file):
    a_df = pd.read_csv(a_file)
    b_df = pd.read_csv(b_file)
    merged_df = pd.concat([a_df, b_df], ignore_index=True)
    merged_df.to_csv(output_file, index=False)


ovis_training_csv = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training.csv'
ovis_valid_csv = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid.csv'
mot17_training_csv = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.csv'
mot17_valid_csv = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.csv'

# merge_csv_files(b2, d2, ovis_training_csv)
# merge_csv_files(d3, b3, mot17_training_csv)
# merge_csv_files(h3, f3, mot17_valid_csv)


def merge_ovis_valid_csv_files():
    a_df = pd.read_csv(f2)  # Video,QID,Language Query,Type,IDs,Start,End,Revision
    b_df = pd.read_csv(h2)  # ID mark frame,Video,QID,Language Query,Type,IDs,Start,End,Revision
    a_df['ID mark frame'] = pd.NA
    a_df = a_df[['ID mark frame', 'Video', 'QID', 'Language Query', 'Type', 'IDs', 'Start', 'End', 'Revision']]

    merged_df = pd.concat([a_df, b_df], ignore_index=True)
    merged_df['ID mark frame'] = merged_df['ID mark frame'].fillna(-1)
    merged_df['ID mark frame'] = merged_df['ID mark frame'].astype(int)
    merged_df['ID mark frame'] = merged_df['ID mark frame'].replace(-1, '')

    merged_df.to_csv(ovis_valid_csv, index=False)


# merge_ovis_valid_csv_files()


def csv_to_json(csv_file_path, json_file_path):
    csv_data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    with open(json_file_path, 'w') as json_file:
        json.dump(csv_data, json_file, indent=4)


ovis_training_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training.json'
ovis_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid.json'
mot17_training_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.json'
mot17_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.json'

# csv_to_json(ovis_training_csv, ovis_training_json)
# csv_to_json(ovis_valid_csv, ovis_valid_json)
# csv_to_json(mot17_training_csv, mot17_training_json)
# csv_to_json(mot17_valid_csv, mot17_valid_json)

mot20_training_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training.json'
mot20_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid.json'
csv_to_json(m3, mot20_training_json)
csv_to_json(n3, mot20_valid_json)


def get_videos(file_path):
    videos = set()
    with open(file_path, 'r') as file:
        data = json.load(file)

    for entry in data:
        video_name = entry['Video']
        videos.add(video_name)

    videos_list = list(videos)
    file_name_without_extension = os.path.splitext(file_path)[0]
    video_name_path = file_name_without_extension + '-videos-name.json'
    with open(video_name_path, 'w') as json_file:
        json.dump(videos_list, json_file)

    return list(videos)


print(f"All ovis train videos ({len(get_videos(ovis_training_json))}): {get_videos(ovis_training_json)}")
print(f"All ovis valid videos ({len(get_videos(ovis_valid_json))}): {get_videos(ovis_valid_json)}")
print(f"All mot17 train videos ({len(get_videos(mot17_training_json))}): {get_videos(mot17_training_json)}")
print(f"All mot17 valid videos ({len(get_videos(mot17_valid_json))}): {get_videos(mot17_valid_json)}")
print(f"All mot20 train videos ({len(get_videos(mot20_training_json))}): {get_videos(mot20_training_json)}")
print(f"All mot20 valid videos ({len(get_videos(mot20_valid_json))}): {get_videos(mot20_valid_json)}")
