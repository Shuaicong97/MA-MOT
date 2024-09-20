# First step: get train and valid videos
import pandas as pd
import json
import csv
import os
import shutil


# OVIS -----
a = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS(Seenat).csv'
b2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/OVIS(Seenat).csv'
c = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS(Ashiq).csv'
d2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/OVIS(Ashiq).csv'
e = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS-Test(Seenat).csv'
f2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/OVIS-Test(Seenat).csv'
g = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - OVIS-Test(Ashiq).csv'
h2 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/OVIS-Test(Ashiq).csv'

# MOT17 -----
a1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT17(Ashiq).csv'
b3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT17(Ashiq).csv'
c1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT17(Seenat).csv'
d3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT17(Seenat).csv'
e1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT17-Test(Ashiq).csv'
f3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT17-Test(Ashiq).csv'
g1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT17-Test(Seenat).csv'
h3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT17-Test(Seenat).csv'

# MOT20 -----
m1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT20(Ashiq).csv'
m3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT20(Ashiq).csv'
n1 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Original/Grounded Tracking Annotations - MOT20(Seenat).csv'
n3 = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/Cleaned/MOT20(Seenat).csv'


# Remove all invalid entries
def clean_csv_file(data_type, input_file, output_file):
    df = pd.read_csv(input_file)
    # remove all columns where the name is blank
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    if 'Language Query' in df.columns:
        df['Language Query'] = df['Language Query'].str.strip()
    if 'IDs' in df.columns:
        df = df[~df['IDs'].astype(str).str.contains('69X')]
    # reformat value type to int
    int_columns = ['ID mark frame', 'QID', 'IDs', 'Start', 'End', 'Query ID', 'Start Frame', 'End Frame']
    for column in int_columns:
        if column in df.columns:
            df[column] = df[column].astype(pd.Int64Dtype())
    if data_type == 'mot17':
        df = df[df['Track ID'].notna() & df['Start Frame'].notna() & df['End Frame'].notna()]
    elif data_type in ['ovis', 'mot20']:
        df = df[df['IDs'].notna() & df['Start'].notna() & df['End'].notna()]

    df.to_csv(output_file, index=False)


# only need to be done once at the first
clean_csv_file('ovis', a, b2)
clean_csv_file('ovis', c, d2)
clean_csv_file('ovis', e, f2)
clean_csv_file('ovis', g, h2)
clean_csv_file('mot17', a1, b3)
clean_csv_file('mot17', c1, d3)
clean_csv_file('mot17', e1, f3)
clean_csv_file('mot17', g1, h3)
clean_csv_file('mot20', m1, m3)
clean_csv_file('mot20', n1, n3)


def merge_csv_files(a_file, b_file, output_file):
    a_df = pd.read_csv(a_file)
    b_df = pd.read_csv(b_file)
    merged_df = pd.concat([a_df, b_df], ignore_index=True)
    merged_df.to_csv(output_file, index=False)


ovis_training_csv = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-training.csv'
ovis_valid_csv = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/OVIS-valid.csv'
mot17_training_csv = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-training.csv'
mot17_valid_csv = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT17-valid.csv'

merge_csv_files(b2, d2, ovis_training_csv)
merge_csv_files(d3, b3, mot17_training_csv)
merge_csv_files(h3, f3, mot17_valid_csv)


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


merge_ovis_valid_csv_files()


def copy_and_rename_file(source_file, destination_file):
    try:
        shutil.copy2(source_file, destination_file)
        print(f"File has been copied from {source_file} to {destination_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

mot20_training_csv = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training.csv'
mot20_valid_csv = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid.csv'
copy_and_rename_file(m3, mot20_training_csv)
copy_and_rename_file(n3, mot20_valid_csv)

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
mot20_training_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-training.json'
mot20_valid_json = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Ours/MOT20-valid.json'

videos = [ovis_training_json, ovis_valid_json, mot17_training_json, mot17_valid_json, mot20_training_json, mot20_valid_json]

csv_to_json(ovis_training_csv, ovis_training_json)
csv_to_json(ovis_valid_csv, ovis_valid_json)
csv_to_json(mot17_training_csv, mot17_training_json)
csv_to_json(mot17_valid_csv, mot17_valid_json)
csv_to_json(mot20_training_csv, mot20_training_json)
csv_to_json(mot20_valid_csv, mot20_valid_json)
