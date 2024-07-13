import os
import subprocess
import sys
import urllib.parse
import time
import pygetwindow as gw

def generate_html(directory):
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']
    directory_name = os.path.basename(directory)
    quoted_directory_name = urllib.parse.quote(directory_name)
    decoded_directory_name = urllib.parse.unquote(quoted_directory_name)
    html_content = f'''<!DOCTYPE HTML>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Directory listing for {decoded_directory_name}/</title>
<script>
function resizeWindow() {{
    window.moveTo(111, 14);
    window.resizeTo(1713, 1027);
}}
window.onload = resizeWindow;
</script>
</head>
<body>
<fieldset>
'''

    for filename in sorted(os.listdir(directory)):
        if any(filename.lower().endswith(ext) for ext in image_extensions):
            html_content += f'<br><br><img src="{filename}" width="800"><br><br>\n'

    html_content += '''</fieldset>
</body>
</html>
'''

    html_filename = os.path.join(directory, f'{directory_name}.html')
    with open(html_filename, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)

    print(f'HTML file "{html_filename}" generated successfully.')

    http_server_cmd = ["python", "-m", "http.server", "8000", "--directory", directory]
    http_server_proc = subprocess.Popen(http_server_cmd)

    local_url = f'http://localhost:8000/{quoted_directory_name}.html'
    chrome_cmd = [r'D:\Program\Chrome\Application\chrome.exe', r'--user-data-dir=D:\2', '--new-window', '--app=' + local_url]
    chrome_proc = subprocess.Popen(chrome_cmd)
    
    time.sleep(3)  # Wait for the window to fully open

    try:
        while True:
            windows = gw.getWindowsWithTitle(f'Directory listing for {decoded_directory_name}/')
            if not windows:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        http_server_proc.terminate()
        print('HTTP server terminated.')
        # Delete the generated HTML file
        try:
            os.remove(html_filename)
            print(f'HTML file "{html_filename}" deleted successfully.')
        except OSError as e:
            print(f'Error deleting file {html_filename}: {e}')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    generate_html(directory_path)
