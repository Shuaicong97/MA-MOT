import ffmpeg
import os

def get_video_length_ffmpeg(video_path):
    """获取视频时长（单位：秒），使用 ffmpeg 解析元数据"""
    try:
        probe = ffmpeg.probe(video_path)
        duration = float(probe['format']['duration'])
        return duration
    except Exception as e:
        print(f"读取 {video_path} 失败: {e}")
        return None

def find_avi_videos_ffmpeg(folder_path):
    """查找所有 AVI 文件并获取它们的时长"""
    avi_files = [f for f in os.listdir(folder_path) if f.endswith('.avi')]
    video_lengths = []

    for avi in avi_files:
        video_path = os.path.join(folder_path, avi)
        length = get_video_length_ffmpeg(video_path)
        if length is not None:
            video_lengths.append((avi, length))

    # 按时长降序排序
    video_lengths.sort(key=lambda x: x[1], reverse=True)
    return video_lengths

# 你的 AVI 文件夹路径
folder_path = "/Users/shuaicongwu/Downloads/YouTubeClips"
video_info = find_avi_videos_ffmpeg(folder_path)

for video, length in video_info:
    print(f"{video}: {length:.2f} 秒")
