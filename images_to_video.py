import os,sys
import cv2
import glob
import psutil
import ffmpegcv


video_folder = '/Users/shuaicongwu/Documents/study/Master/MA/data/output'
videos = [x[0] for x in os.walk(video_folder)]

# generate videos from images failed.
for i, v in enumerate(videos[1:]):
    print(i, v)
    images = []
    imgs = glob.glob(f"{v}/*.jpg")
    imgs = [e for e in imgs if 'mini' not in e]
    imgs = sorted(imgs, key=lambda e: int((e.split('/')[-1].split('-')[-1].split('.')[0])))
    for img in imgs:
        if 'mini' not in img:
            # print(img)
            images.append(os.path.join(video_folder,img))

    video_name = f'/Users/shuaicongwu/Documents/study/Master/MA/data/ovis_videos/{v.split("/")[-1]}.avi'

    dir_path = os.getcwd()
    shape = (640, 480)
    fps = 5.0

    print(images)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #video = cv2.VideoWriter(video_name, fourcc, fps, shape)
    video = ffmpegcv.VideoWriter(video_name,None,fps)
    for image in images:
        try:
            image_path = os.path.join(dir_path, image)
            frame = cv2.imread(image_path)
            # resized=cv2.resize(frame,shape)
            video.write(frame)
        except Exception as e:
            print(f"Error writing frame: {e}")
        # process = psutil.Process()
        # memory_usage = process.memory_info().rss
        # memory_usage_mb = memory_usage / (1024 * 1024)

        # print(f'Estimated memory usage of cv2.VideoWriter object: {memory_usage_mb:.2f} MB')
    video.release()
   # cv2.destroyAllWindows()
    print(f"Video created: {video_name}")

