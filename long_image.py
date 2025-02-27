# 需要安装 pywin32 库：  pip install pywin32
# 该代码仅在 Windows 平台有效。

import sys
import subprocess
import time
from PIL import Image, ImageOps
import ctypes
import win32gui
import win32con
import re
import os
import urllib.parse

def find_chrome_window(title_pattern):
    """查找匹配指定标题模式的 Chrome 窗口句柄。"""
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)

            # 尝试解码窗口标题 (先尝试 GBK，再尝试 UTF-16)
            try:
                decoded_title = title.encode('latin1').decode('gbk')  # 尝试 GBK
            except (UnicodeDecodeError, UnicodeEncodeError):
                try:
                    decoded_title = title.encode('latin1').decode('utf-16')  # 尝试 UTF-16
                except (UnicodeDecodeError, UnicodeEncodeError):
                    decoded_title = title # 如果都失败, 则使用原始标题

            if re.search(title_pattern, decoded_title):  # 使用解码后的标题
                windows.append(hwnd)


    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def open_image_in_chrome(image_path, chrome_exe_path, user_data_dir):
    """
    使用 Chrome 打开图片，窗口大小自适应宽度且高度固定为1000，并居中显示。
    """
    try:
        # 获取图片原始尺寸和文件名
        img = Image.open(image_path)
        original_width, original_height = img.size
        img = ImageOps.exif_transpose(img)  # 修正EXIF旋转
        file_name = os.path.basename(image_path)
        name_without_ext = os.path.splitext(file_name)[0]

        # 计算自适应宽度（高度固定为1000）
        new_width = int(original_width * (1000 / original_height))
        new_width = max(original_width, 100)  # 最小宽度限制

        # 增加宽度补偿
        width_compensation = 34
        new_width += width_compensation

        # 获取屏幕尺寸
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

        # 计算居中位置
        new_x = (screen_width - new_width) // 2
        new_y = (screen_height - 1000) // 2

        # 构建正确的 file:/// URL
        image_path = image_path.replace('\\', '/')
        encoded_image_path = urllib.parse.quote(image_path, safe='/')
        file_url = f'file:///{encoded_image_path}'

        # 构建Chrome命令（使用 --app 模式）
        chrome_cmd = [
            chrome_exe_path,
            f'--user-data-dir={user_data_dir}',
            '--new-window',
            f'--app={file_url}',
        ]

        # 启动 Chrome 进程
        process = subprocess.Popen(chrome_cmd)
        if process.returncode is not None:
            print(f"错误：Chrome 进程启动失败，返回码：{process.returncode}")
            sys.exit(1)


        # 构建更宽容的窗口标题模式 (只匹配文件名的前几个字符, 至少匹配2个字符)
        title_pattern = re.escape(name_without_ext[:2]) # 取文件名前2个字符
        if len(name_without_ext) > 2: #如果文件名字符数大于2，则尝试增加匹配字符数
            for i in range(3, len(name_without_ext) + 1):
              temp_pattern = re.escape(name_without_ext[:i])
              if find_chrome_window(temp_pattern): # 只要找到就停止增加
                  title_pattern = temp_pattern
                  break

        # 等待 Chrome 窗口出现 (最多等待5秒)
        start_time = time.time()
        chrome_windows = []

        while not chrome_windows and time.time() - start_time < 5:
            chrome_windows = find_chrome_window(title_pattern)
            time.sleep(0.1)

        if not chrome_windows:
            print("错误：未找到 Chrome 窗口。")
            sys.exit(1)

        # 获取找到的第一个窗口句柄
        hwnd = chrome_windows[0]

        # 使用 SetWindowPos 调整窗口位置和大小
        win32gui.SetWindowPos(
            hwnd,
            win32con.HWND_TOP,
            new_x,
            new_y,
            new_width,
            1000,
            win32con.SWP_SHOWWINDOW,
        )

        print(f"图片已在 Chrome 中打开，窗口位置：({new_x}, {new_y})，大小：({new_width}, 1000)")

    except FileNotFoundError:
        print(f"错误：找不到图片文件 '{image_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误：{e}")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python open_image.py <图片路径>")
        sys.exit(1)

    image_path = sys.argv[1]
    valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')
    if not image_path.lower().endswith(valid_extensions):
        print("错误：不支持的图片格式。支持的格式：", valid_extensions)
        sys.exit(1)

    chrome_exe_path = r'D:\Program\Chrome\Application\chrome.exe'
    user_data_dir = r'D:\2'
    open_image_in_chrome(image_path, chrome_exe_path, user_data_dir)
