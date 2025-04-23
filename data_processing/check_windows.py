import json

def check_vid_duration_in_windows(jsonl_path):
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            vid = data.get("vid", "")
            relevant_windows = data.get("relevant_windows", [])
            relevant_clip_ids = data.get("relevant_clip_ids", [])


            # 提取vid中两个数字
            try:
                parts = vid.split('_')
                start = float(parts[-2])
                end = float(parts[-1])
                vid_duration = int(end - start)
            except Exception as e:
                print(f"Error parsing vid: {vid}, error: {e}")
                continue

            # 遍历relevant_windows，检查是否有等于duration的区间长度
            for window in relevant_windows:
                window_duration = window[1] - window[0]
                if window_duration == vid_duration:
                    # print(f"Match found! qid: {data['qid']}, vid: {vid}, duration: {vid_duration}, window: {window}")
                    break  # 只需找到一个匹配就可以了
            if len(relevant_clip_ids) == 1:
                print(f'vid: {vid}, duration: {vid_duration}, clip_id: {relevant_clip_ids[0]}')

# 使用方式示例（你需要将文件路径替换成实际路径）
check_vid_duration_in_windows("/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/QVHighlight/highlight_train_release_IV2.jsonl")
