import pandas as pd

# 假设CSV文件名为 'data.csv'
file_paths1 = ['../data/Ours/Original/Grounded Tracking Annotations - MOT17(Ashiq).csv',
               '../data/Ours/Original/Grounded Tracking Annotations - MOT17(Seenat).csv',
               '../data/Ours/Original/Grounded Tracking Annotations - MOT17-Test(Ashiq).csv',
               '../data/Ours/Original/Grounded Tracking Annotations - MOT17-Test(Seenat).csv']

file_paths2 = ['../data/Ours/Original/Grounded Tracking Annotations - MOT20(Ashiq).csv',
               '../data/Ours/Original/Grounded Tracking Annotations - MOT20(Seenat).csv',
               '../data/Ours/Original/Grounded Tracking Annotations - OVIS(Ashiq).csv',
               '../data/Ours/Original/Grounded Tracking Annotations - OVIS(Seenat).csv',
               '../data/Ours/Original/Grounded Tracking Annotations - OVIS-Test(Ashiq).csv',
               '../data/Ours/Original/Grounded Tracking Annotations - OVIS-Test(Seenat).csv']

sum_all = 0

for file_path in file_paths1:
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 计算每个Video对应的不同Track ID的数量
    result = df.groupby('Video')['Track ID'].nunique().reset_index()

    # 重命名列
    result.columns = ['Video', 'Unique Track ID Count']

    # 计算总和
    total_count = result['Unique Track ID Count'].sum()
    sum_all += total_count
    # 显示结果
    # print(result)
    print(f"总共的不同Track ID数量: {total_count}")

for file_path in file_paths2:
    # 读取CSV文件
    df = pd.read_csv(file_path)

    # 计算每个Video对应的不同Track ID的数量
    result = df.groupby('Video')['IDs'].nunique().reset_index()

    # 重命名列
    result.columns = ['Video', 'Unique Track ID Count']

    # 计算总和
    total_count = result['Unique Track ID Count'].sum()
    sum_all += total_count
    # 显示结果
    # print(result)
    print(f"总共的不同Track ID数量: {total_count}")

print(f"所有数据集下的不同Track ID数量: {sum_all}")  # 4519
