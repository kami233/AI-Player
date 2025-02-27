import os
import sys
import shutil
import tempfile
import subprocess
from PIL import Image

# --- 全局配置 ---
BASE_DIR = "D:\\Epic\\Animesave\\hev-ren1_20220312_0911.35401"  # 基础路径
CHROME_OPEN_SCRIPT = os.path.join(BASE_DIR, "open_image_with_chrome.py")  # Chrome打开脚本
WATERFALL_SP_SCRIPT = os.path.join(BASE_DIR, "waterfall_sp.py")  # waterfall_sp.py 脚本
FFPLAYAGI_BAT = "C:\\Users\\Administrator\\Desktop\\ffplayAGI.bat"  # ffplayAGI.bat 路径

# 支持的图片文件类型
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']

def count_images_in_files(files):
    """计算文件列表中的图片数量"""
    return sum(1 for file in files if os.path.splitext(file)[1].lower() in IMAGE_EXTENSIONS)

def copy_images_to_temp_dir(files, temp_dir):
    """将文件列表中的图片复制到临时目录"""
    for file in files:
        shutil.copy(file, temp_dir)  # 目标路径已包含文件名，无需 os.path.join

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file1> <file2> ...")
        return

    all_files = sys.argv[1:]

    # 分离.ans文件和其他文件
    ans_files = [f for f in all_files if f.lower().endswith('.ans')]
    other_files = [f for f in all_files if f not in ans_files]

    # 处理.ans文件
    for ans_file in ans_files:
        subprocess.run([
            'powershell.exe',
            '-NoExit',
            '-Command',
            f'$Host.UI.RawUI.BackgroundColor = "Black"; Get-Content "{os.path.abspath(ans_file)}" -Raw'
        ])

    # 处理其他文件
    if other_files:
        num_images = count_images_in_files(other_files)

        if num_images == 1:
            # 只有一张图片，检查宽高比
            img_path = other_files[0]
            try:
                img = Image.open(img_path)
                if img.height > img.width * 3:
                    subprocess.run([sys.executable, CHROME_OPEN_SCRIPT, img_path])
                    return
            except (FileNotFoundError, Image.UnidentifiedImageError):
                print(f"Error: Could not open or read image file: {img_path}")
            # 不满足宽高比或读取失败，都执行 ffplayAGI.bat
            subprocess.run([FFPLAYAGI_BAT] + other_files)

        elif num_images > 3:
            # 多张图片，使用 waterfall_sp.py
            temp_dir = tempfile.mkdtemp()
            print(f"Created temporary directory: {temp_dir}")
            try:
                copy_images_to_temp_dir(other_files, temp_dir)
                subprocess.run([sys.executable, WATERFALL_SP_SCRIPT, temp_dir]) # 明确指定 python 解释器
            finally:
                shutil.rmtree(temp_dir)
                print(f"Deleted temporary directory: {temp_dir}")
        else:
            # 0, 2, 3 张图片，使用 ffplayAGI.bat
            if other_files: # 再次检查, 确保列表不是空的
                subprocess.run([FFPLAYAGI_BAT] + other_files)

if __name__ == "__main__":
    main()
