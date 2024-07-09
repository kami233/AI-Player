import sys
import zipfile
import rarfile
import tempfile
import os
import subprocess
import shutil
from PIL import Image

# 新增支持的文件类型列表
SUPPORTED_EXTENSIONS = ['.jpg', '.png', '.bmp', '.jpeg', '.gif',
                        '.mp4', '.flv', '.mkv', '.m2ts', '.wemp',
                        '.mp3', '.wav', '.m4a', '.aac']

def extract_files_to_single_folder(zip_file_path, supported_extensions):
    temp_dir = tempfile.mkdtemp()  # 创建临时文件夹
    output_folder = os.path.join(temp_dir, "extracted_files")
    os.makedirs(output_folder)  # 创建存放解压文件的文件夹
    print(f"Extracting files from {zip_file_path} to {output_folder}")

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for file_info in zip_file.infolist():
            if any(file_info.filename.lower().endswith(ext) for ext in supported_extensions):
                # 构建完整的文件路径
                file_path = os.path.join(output_folder, os.path.basename(file_info.filename))
                # 解压文件到输出文件夹
                with open(file_path, 'wb') as f:
                    f.write(zip_file.read(file_info.filename))

    return output_folder

def extract_files_to_single_folder_rar(rar_file_path, supported_extensions):
    temp_dir = tempfile.mkdtemp()  # 创建临时文件夹
    output_folder = os.path.join(temp_dir, "extracted_files")
    os.makedirs(output_folder)  # 创建存放解压文件的文件夹
    print(f"Extracting files from {rar_file_path} to {output_folder}")

    with rarfile.RarFile(rar_file_path, 'r') as rar_file:
        for file_info in rar_file.infolist():
            if any(file_info.filename.lower().endswith(ext) for ext in supported_extensions):
                # 构建完整的文件路径
                file_path = os.path.join(output_folder, os.path.basename(file_info.filename))
                # 解压文件到输出文件夹
                with open(file_path, 'wb') as f:
                    f.write(rar_file.read(file_info.filename))

    return output_folder

def open_folder_with_script(folder_path, script_path):
    # 构建完整的命令列表
    command = ['python', script_path, folder_path]
    # 执行指定的脚本来打开文件夹
    subprocess.run(command, shell=True)

def delete_temp_folder(temp_dir):
    shutil.rmtree(temp_dir)  # 删除临时文件夹及其内容

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python view_compressed_files.py <path_to_compressed_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if file_path.endswith('.zip'):
        temp_dir = extract_files_to_single_folder(file_path, SUPPORTED_EXTENSIONS)
    elif file_path.endswith('.rar'):
        temp_dir = extract_files_to_single_folder_rar(file_path, SUPPORTED_EXTENSIONS)
    else:
        print("Unsupported file format. Only .zip and .rar are supported.")
        sys.exit(1)

    print(f"Press enter to delete temporary folder {temp_dir}")
    
    # 使用指定的脚本打开文件夹
    open_folder_with_script(temp_dir, r'D:\Epic\Animesave\hev-ren1_20220312_0911.35401\waterfall_sp.py')

    # 等待用户确认完成查看文件后按下回车键
    # input("Press Enter to delete temporary folder...")

    # 删除临时文件夹
    delete_temp_folder(temp_dir)
    print(f"Temporary folder {temp_dir} deleted.")
