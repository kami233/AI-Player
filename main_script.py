import sys
import os
import subprocess

def handle_zip_rar(file_path):
    # Call view_compressed.py to handle .zip and .rar files
    script_path = r"D:\Epic\Animesave\hev-ren1_20220312_0911.35401\view_compressed.py"
    subprocess.run(["python", script_path, file_path])

def handle_non_zip_rar(file_paths):
    # Call process_files.py to handle non .zip and .rar files
    script_path = r"D:\Epic\Animesave\hev-ren1_20220312_0911.35401\process_files.py"
    subprocess.run(["python", script_path] + file_paths)

def handle_folder(folder_path):
    # Call waterfall_sp.py to handle folders
    script_path = r"D:\Epic\Animesave\hev-ren1_20220312_0911.35401\waterfall_sp.py"
    subprocess.run(["python", script_path, folder_path])

def main(args):
    if len(args) < 2:
        print("Usage: python main_script.py <file_or_folder_path>")
        return

    paths = args[1:]

    zip_rar_files = []
    non_zip_rar_files = []
    folders = []

    # Classify paths into zip/rar files, non-zip/rar files, and folders
    for path in paths:
        if os.path.isfile(path):
            if path.lower().endswith(('.zip', '.rar')):
                zip_rar_files.append(path)
            else:
                non_zip_rar_files.append(path)
        elif os.path.isdir(path):
            folders.append(path)
        else:
            print(f"Invalid path: {path}")

    # Handle folders
    for folder in folders:
        handle_folder(folder)

    # Handle .zip and .rar files
    for zip_rar_file in zip_rar_files:
        handle_zip_rar(zip_rar_file)

    # Handle non .zip and .rar files
    if non_zip_rar_files:
        handle_non_zip_rar(non_zip_rar_files)

if __name__ == "__main__":
    main(sys.argv)
