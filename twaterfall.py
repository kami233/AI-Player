import os
import sys
import glob
import subprocess
import shutil
import tempfile
from PIL import Image
import random

# 定义脚本路径
scriptPath = "D:\\Epic\\Animesave\\hev-ren1_20220312_0911.35401\\"
batPath = "C:\\Users\\Administrator\\Desktop\\"

def calculate_score(image_path):
    # 计算图片的分数
    img = Image.open(image_path)
    width, height = img.size
    score = 0
    
    if height > width:
        score = 2
    elif width > height:
        score = 1
    
    return score

def batch_process_images(folder_path, batch_size=50):
    # 获取文件夹下的所有图片文件路径
    image_files = []
    for ext in ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'):
        image_files.extend(glob.glob(os.path.join(folder_path, '*' + ext)))
    
    total_images = len(image_files)
    print(f"Total images found in '{folder_path}': {total_images}")

    if total_images == 0:
        print("No images found in the specified folder.")
        return
    
    # 创建临时文件夹
    temp_dir = tempfile.mkdtemp()

    try:
        selected_images = []
        remaining_images = image_files[:]
        batch_index = 0
        
        while remaining_images:
            selected_batch = []
            batch_score = 0
            for img_file in remaining_images[:batch_size]:
                img_score = calculate_score(img_file)
                batch_score += img_score
                selected_batch.append(img_file)
                
                if batch_score >= 30:
                    break
            
            # 创建批次的临时目录
            batch_temp_dir = os.path.join(temp_dir, f"batch_{batch_index}")
            os.makedirs(batch_temp_dir)
            
            # 复制选中的图片到批次临时目录中
            for img_file in selected_batch:
                shutil.copy(img_file, batch_temp_dir)
                selected_images.append(img_file)
                remaining_images.remove(img_file)
            
            # 根据批次的分数选择不同的处理脚本
            if batch_score > 20:
                subprocess.run(['python', os.path.join(scriptPath, 'waterfall.py'), batch_temp_dir])
            elif 13 <= batch_score <= 20:
                subprocess.run(['python', os.path.join(scriptPath, 'waterfall_5col.py'), batch_temp_dir])
            elif 7 <= batch_score <= 12:
                subprocess.run(['python', os.path.join(scriptPath, 'waterfall_4col.py'), batch_temp_dir])
            elif 4 <= batch_score <= 6:
                subprocess.run(['python', os.path.join(scriptPath, 'waterfall_3col.py'), batch_temp_dir])
            else:
                subprocess.run([os.path.join(batPath, 'ffplayAI.bat'), batch_temp_dir], shell=True)
            
            batch_index += 1
    
    finally:
        # 删除临时文件夹及其内容
        shutil.rmtree(temp_dir)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python batch_image_processing.py <folder_path>")
        sys.exit(1)
    
    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        print(f"Error: '{folder_path}' is not a valid directory.")
        sys.exit(1)

    # 检查文件夹中的图片数量
    image_count = len(glob.glob(os.path.join(folder_path, '*.*')))
    print(f"Total images detected in '{folder_path}': {image_count}")

    # 如果图片数量超过50，进行分批次处理
    if image_count > 22:
        python_executable = sys.executable  # 获取当前Python解释器路径
        subprocess.run([python_executable, os.path.join(scriptPath, 'waterfall_local_auto.py'), folder_path])
        print("Number of images is greater than 22. Using waterfall_local.py.")
    elif image_count > 3:
        batch_process_images(folder_path)
    else:
        try:
            subprocess.run(['python', os.path.join(scriptPath, 'waterfall_local_auto.py'), folder_path], check=True)
            print("Number of images is less than or equal to 50. Not batching.")
        except subprocess.CalledProcessError:
            print("First subprocess call failed. Running second command.")
            subprocess.run([os.path.join(batPath, 'ffplayAI.bat'), folder_path])
