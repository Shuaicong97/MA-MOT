#!/bin/bash
echo "🚀 脚本开始执行了！"

# 设置输入目录（可通过参数传入，默认当前目录）
json_file="/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data_processing/report/ovis_info_train_533.txt"
input_dir="/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/OVIS/train"
output_dir="/Users/shuaicongwu/Documents/study/Master/MA/MA-MOT/data/ovis_videos/train"

# 确保输出目录存在
mkdir -p "$output_dir"
exclude=("86a88668" "af48b2f9" "2fb5a55b" "cfff47c3")

# 读取 folders.txt 一行一行
while IFS= read -r folder_name; do
  # 忽略空行
  [ -z "$folder_name" ] && continue

  echo "现在处理: $folder_name"

  # 检查是否在排除列表中
  if [[ " ${exclude[*]} " =~ " $folder_name " ]]; then
    echo "🚫 排除文件夹: $folder_name"
    continue
  fi

  folder="$input_dir/$folder_name"

  # 确保子文件夹存在
  if [ ! -d "$folder" ]; then
    echo "❌ 文件夹不存在: $folder"
    continue
  fi

  # 获取照片总数（*.jpg）
  count=$(ls "$folder"/*.jpg 2>/dev/null | wc -l)

  if [ "$count" -eq 0 ]; then
    echo "⚠️ 目录 $input_dir 中没有找到jpg图片。"
    continue  # 跳过当前文件夹
  fi

  last_frame=$(printf "%06d" "$count")
  added_frame_path=""

  # 判断奇偶决定使用多少帧：偶数不变，奇数加1
  if [ $((count % 2)) -eq 0 ]; then
    frames=$count
  else
    frames=$((count + 1))
    next_frame=$(printf "%06d" "$frames")
    cp "$folder/${last_frame}.jpg" "$folder/${next_frame}.jpg"
    added_frame_path="$folder/${next_frame}.jpg"
  fi

  # 生成输出文件名
  output_file="${folder_name}_0.0_${frames}.0.mp4"
  output_path="$output_dir/$output_file"

  echo "🖼️ 总照片数: $count"
  echo "🎞️ 使用帧数: $frames"
  echo "💾 输出文件: $output_path"

  # 调用 ffmpeg
  ffmpeg -framerate 1 -start_number 1 \
    -i "$folder/img_%07d.jpg" \
    -frames:v $frames -r 1 -pix_fmt yuv420p \
    "$output_path"

  # 删除临时添加的帧
  if [ -n "$added_frame_path" ]; then
    rm "$added_frame_path"
    echo "🧹 已删除添加的补帧: $added_frame_path"
  fi

done < "$json_file"