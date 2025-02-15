import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict

def is_number(value):
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def extract_data(csv_file):
    extracted_data = []
    auc_count = 0

    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            seq_value = row['seq']
            auc_value = row.get('HOTA___AUC', None)  # 获取HOTA___AUC列的值

            if auc_value is not None and seq_value != 'COMBINED':
                if is_number(auc_value):
                    auc_count += 1
                    auc_value = float(auc_value)  # 确保是数值
                    str_part = seq_value.split('+', 1)[-1]  # 获取加号后面的部分
                    extracted_data.append((str_part, len(str_part), auc_value))
                else:
                    print(f"Invalid AUC value (not a number): {auc_value}")  # 打印非数值的字符串

    print(f"\n🔢 **非空 HOTA_AUC 总行数: {auc_count}**")  # 输出统计值
    return extracted_data

def plot_data(data):
    lengths = [item[1] for item in data]
    auc_values = [item[2] for item in data]

    plt.figure(figsize=(10, 6))
    sns.regplot(x=lengths, y=auc_values, scatter=True, fit_reg=True, scatter_kws={'alpha': 0.3, 's': 10})
    plt.xlabel('Length of query')
    plt.ylabel('Accuracy (HOTA___AUC)')
    plt.title('Query Length vs Accuracy')
    plt.grid(True)

    plt.savefig('query_length_vs_accuracy.png', dpi=300, bbox_inches='tight')  # 设置高分辨率并优化边距
    plt.close()  # 关闭 plt，避免显示窗口

def count_auc_intervals(data, interval=0.1):
    """ 统计各个HOTA_AUC区间（0-0.1, 0.1-0.2, ..., 0.8-0.9等）的对象数量 """
    auc_values = [item[2] for item in data]  # 只提取AUC数据
    bins = np.arange(0.1, 1.1, interval)  # 生成 [0, 0.1, 0.2, ..., 1.0] 的区间

    count_dict = defaultdict(int)
    count_zero = 0  # 统计等于 0 的值
    count_zero_to_point1 = 0  # 统计 (0, 0.1] 的值

    for value in auc_values:
        if value == 0:
            count_zero += 1  # 等于 0 的单独统计
        elif 0 < value <= 0.1:
            count_zero_to_point1 += 1  # (0, 0.1] 之间的统计
        else:
            for i in range(len(bins) - 1):
                if bins[i] <= value < bins[i + 1]:  # 确保 AUC 值在该区间
                    count_dict[(bins[i], bins[i + 1])] += 1
                    break

    total_count = count_zero + count_zero_to_point1 + sum(count_dict.values())

    # 打印统计结果
    print("\n### HOTA_AUC 区间统计 ###")
    print(f"0.0: {count_zero} 个")  # 单独打印 0 的数量
    print(f"(0.0, 0.1]: {count_zero_to_point1} 个")  # 单独打印 (0, 0.1] 的数量
    for (low, high), count in sorted(count_dict.items()):
        print(f"{low:.1f} - {high:.1f}: {count} 个")

    print(f"\n🔢 **总对象数: {total_count}**")


# 示例调用
csv_file_path = 'pedestrian_detailed.csv'  # 请替换为你的CSV文件路径
data = extract_data(csv_file_path)
print(data)
count_auc_intervals(data)
plot_data(data)
