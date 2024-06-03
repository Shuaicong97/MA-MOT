import os
import re
import shutil


def rename_jpeg_files():
    main_dir = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/ovis/valid/JPEGImages'

    for subdir in os.listdir(main_dir):
        subdir_path = os.path.join(main_dir, subdir)
        if os.path.isdir(subdir_path):
            jpg_files = [f for f in os.listdir(subdir_path) if f.endswith('.jpg')]

            for idx, jpg_file in enumerate(sorted(jpg_files)):
                match = re.match(r'img_(\d+)\.jpg', jpg_file)
                if match:
                    new_name = f"{idx + 1:05}.jpg"
                    old_file_path = os.path.join(subdir_path, jpg_file)
                    new_file_path = os.path.join(subdir_path, new_name)

                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed {old_file_path} to {new_file_path}")


def compress_folders(main_folder, output_folder, batch_size=20):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    subdirs = [d for d in os.listdir(main_folder) if os.path.isdir(os.path.join(main_folder, d))]

    for i in range(0, len(subdirs), batch_size):
        batch = subdirs[i:i + batch_size]
        batch_name = f"batch_{i // batch_size + 1}.zip"
        batch_path = os.path.join(output_folder, batch_name)

        # create temporary directory
        temp_dir = os.path.join(main_folder, 'temp_compress_dir')
        os.makedirs(temp_dir, exist_ok=True)

        # copy sub directories to the temporary directory
        for subdir in batch:
            src = os.path.join(main_folder, subdir)
            dst = os.path.join(temp_dir, subdir)
            shutil.copytree(src, dst)

        shutil.make_archive(batch_path[:-4], 'zip', temp_dir)

        # delete the temporary directory
        shutil.rmtree(temp_dir)

        print(f"Created {batch_path}")


main_folder = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/ovis/train/JPEGImages'
output_folder = '/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/ovis/train'
compress_folders(main_folder, output_folder)
