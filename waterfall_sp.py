import os
import sys

def process_folder(folder_path):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
    video_extensions = ['.mp4', '.flv', '.mkv', '.m2ts', '.wemp', '.mp3', '.wav', '.m4a', '.aac']

    contains_image = False
    contains_video = False

    # Check if the folder contains images or videos
    for root, _, files in os.walk(folder_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() in image_extensions:
                contains_image = True
            elif ext.lower() in video_extensions:
                contains_video = True

    if contains_image and contains_video:
        print(f"Folder contains both images and videos. Processing images first.")
        script_paths = [r"D:\Epic\Animesave\hev-ren1_20220312_0911.35401\twaterfall.py",
                        r"D:\Epic\Animesave\hev-ren1_20220312_0911.35401\video_waterfall.py"]
    elif contains_image:
        script_paths = [r"D:\Epic\Animesave\hev-ren1_20220312_0911.35401\twaterfall.py"]
    elif contains_video:
        script_paths = [r"D:\Epic\Animesave\hev-ren1_20220312_0911.35401\video_waterfall.py"]
    else:
        print(f"No images or videos found in {folder_path}")
        return

    # Execute each script in sequence
    for script_path in script_paths:
        os.system(f"python \"{script_path}\" \"{folder_path}\"")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_folder.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        sys.exit(1)

    process_folder(folder_path)
