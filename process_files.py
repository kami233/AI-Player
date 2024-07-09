import os
import sys
import shutil
import tempfile
import subprocess

# 支持的图片文件类型
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']

def count_images_in_files(files):
    total_images = 0
    for file in files:
        filename, file_extension = os.path.splitext(file)
        if file_extension.lower() in IMAGE_EXTENSIONS:
            total_images += 1
    return total_images

def copy_images_to_temp_dir(files, temp_dir):
    for file in files:
        filename = os.path.basename(file)
        shutil.copy(file, os.path.join(temp_dir, filename))

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file1> <file2> ...")
        return
    
    files = sys.argv[1:]
    num_images = count_images_in_files(files)

    if num_images > 3:
        temp_dir = tempfile.mkdtemp()
        print(f"Created temporary directory: {temp_dir}")
        try:
            copy_images_to_temp_dir(files, temp_dir)
            # 将临时目录路径传递给指定的处理脚本
            subprocess.run(['python', 'D:\\Epic\\Animesave\\hev-ren1_20220312_0911.35401\\waterfall_sp.py', temp_dir])
        finally:
            # 删除临时目录
            shutil.rmtree(temp_dir)
            print(f"Deleted temporary directory: {temp_dir}")
    else:
        # 调用另一个处理程序，传递文件路径作为参数
        subprocess.run(['C:\\Users\\Administrator\\Desktop\\ffplayAI.bat'] + files)

if __name__ == "__main__":
    main()
