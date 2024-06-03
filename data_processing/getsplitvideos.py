# First step: get train and valid videos
import pandas as pd
import json
import csv

seenat_input_file = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/Grounded Tracking Annotations - OVIS(Seenat).csv'
seenat_output_file = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/Clean OVIS(Seenat).csv'
ashiq_input_file = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/Grounded Tracking Annotations - OVIS(Ashiq).csv'
ashiq_output_file = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/Clean OVIS(Ashiq).csv'


def reformat_csv_file(file_path, output_file_path):
    df = pd.read_csv(file_path)
    # remove all columns where the name is blank
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # reformat value type to int
    int_columns = ['QID', 'IDs', 'Start', 'End']
    for column in int_columns:
        if column in df.columns:
            df[column] = df[column].astype(pd.Int64Dtype())
    df.to_csv(output_file_path, index=False)

# only need to be done once at the first
# reformat_csv_file(ashiq_input_file, ashiq_input_file)


def remove_invalid_rows(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
            open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in reader:
            if row['IDs'] and row['Start'] and row['End']:
                writer.writerow(row)

    print(f"Filtered data has been saved to {output_file}")


def process_csv_files(a_file_path, b_file_path, output_combined_path, output_remaining_path):
    # read csv files
    a_df = pd.read_csv(a_file_path)
    b_df = pd.read_csv(b_file_path)

    unique_videos = b_df['Video'].unique()[:129]

    selected_rows = []
    remaining_rows = []

    # select from b file
    for video_name in unique_videos:
        video_group = b_df[b_df['Video'] == video_name]
        selected_rows.append(video_group)

    combined_df = pd.concat([a_df] + selected_rows, ignore_index=True)
    remaining_df = b_df[~b_df['Video'].isin(unique_videos)]

    int_columns = ['QID', 'IDs', 'Start', 'End']
    for column in int_columns:
        if column in combined_df.columns:
            combined_df[column] = combined_df[column].astype(pd.Int64Dtype())
        if column in remaining_df.columns:
            remaining_df.loc[:, column] = remaining_df.loc[:, column].astype(pd.Int64Dtype())

    combined_df.to_csv(output_combined_path, index=False)
    remaining_df.to_csv(output_remaining_path, index=False)


def get_videos(file_path):
    videos = set()
    with open(file_path, 'r') as file:
        data = json.load(file)

    for entry in data:
        video_name = entry['Video']
        videos.add(video_name)

    return list(videos)


def csv_to_json(csv_file_path, json_file_path):
    csv_data = []
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            csv_data.append(row)

    with open(json_file_path, 'w') as json_file:
        json.dump(csv_data, json_file, indent=2)


remove_invalid_rows(seenat_input_file, seenat_output_file)
remove_invalid_rows(ashiq_input_file, ashiq_output_file)

# get json files from csv files
clean_ashiq_all = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/clean_ashiq_all.json'
clean_seenat_all = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/clean_seenat_all.json'
# csv_to_json('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/Clean OVIS(Ashiq).csv', clean_ashiq_all)
# csv_to_json('/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/Clean OVIS(Seenat).csv', clean_seenat_all)


a_file_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/Clean OVIS(Ashiq).csv'
b_file_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/Clean OVIS(Seenat).csv'
output_combined_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/processed_train.csv'
output_remaining_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/processed_valid.csv'

process_csv_files(a_file_path, b_file_path, output_combined_path, output_remaining_path)

train_json_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/ovis_train.json'
valid_json_path = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/generated_by_code/ovis_json/ovis_valid.json'

csv_to_json(output_combined_path, train_json_path)
csv_to_json(output_remaining_path, valid_json_path)


print(f"All train videos ({len(get_videos(train_json_path))}): {get_videos(train_json_path)}")
print(f"All valid videos ({len(get_videos(valid_json_path))}): {get_videos(valid_json_path)}")
