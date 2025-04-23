import os
import json

jsonl_path = "data/QVHighlight/highlight_train_release_IV2.jsonl"  # 替换为你的 jsonl 文件路径

with open(jsonl_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line.strip())
        relevant_windows = data.get("relevant_windows")
        duration = data.get("duration")
        query = data.get("query")
        if duration % 2 != 0:
            print(f"在查询 {query} 中找到奇数值: {num} 在窗口 {window}")
        for window in relevant_windows:
            # 检查数组中的每个数字是否为奇数
            for num in window:
                if num % 2 != 0:  # 如果是奇数
                    print(f"在查询 {query} 中找到奇数值: {num} 在窗口 {window}")


print('done')