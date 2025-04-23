import cv2
import os
from glob import glob

# 设置文件夹路径
image_folder = "/Users/shuaicongwu/Desktop/Hallucination VLM/240P/tt2334873_clip"  # 你的图片文件夹
output_path = "/Users/shuaicongwu/Desktop/Hallucination VLM/240P/tt2334873_clip/tt2334873_clip.mp4"  # 保存路径
# fps = 109/(8*60+31)  # 4s per image
# fps = 432/(7*60+59)  #
fps = 117/(9*60+14)

# 获取所有图片
images = sorted(glob(os.path.join(image_folder, "*.jpg")))

# 读取第一张图片获取尺寸
frame = cv2.imread(images[0])
height, width, layers = frame.shape

# 创建输出文件夹（如果不存在）
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# 创建视频写入对象
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# 逐帧写入
for image in images:
    frame = cv2.imread(image)
    video.write(frame)

# 释放资源
video.release()
cv2.destroyAllWindows()

print(f"视频已保存到: {output_path}")
