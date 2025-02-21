import os
import shutil

def clean_folders(root_folder):
    # 遍历 root_folder 下的所有子文件夹
    for subdir in os.listdir(root_folder):
        subdir_path = os.path.join(root_folder, subdir)

        # 确保是文件夹
        if os.path.isdir(subdir_path):
            img1_path = os.path.join(subdir_path, "img1")

            # 删除 img1 文件夹
            if os.path.exists(img1_path) and os.path.isdir(img1_path):
                shutil.rmtree(img1_path)
                print(f"Deleted: {img1_path}")

            # # 遍历子文件夹中的所有内容，删除除 gt 之外的文件/文件夹
            # for item in os.listdir(subdir_path):
            #     item_path = os.path.join(subdir_path, item)
            #     if item != "gt":  # 只保留 gt 文件夹
            #         if os.path.isdir(item_path):
            #             shutil.rmtree(item_path)
            #         else:
            #             os.remove(item_path)
            #         print(f"Deleted: {item_path}")

if __name__ == "__main__":
    root_folder = "/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/Filtered Results by Annotation V2"  # 你的文件夹路径
    clean_folders(root_folder)
