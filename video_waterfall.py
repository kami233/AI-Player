import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import subprocess

class WaterfallViewer:
    def __init__(self, master, folder_path):
        self.master = master
        self.folder_path = folder_path
        self.media_files = []
        self.media_labels = []
        self.padding = 10  # Padding between items
        self.current_row = 0
        self.columns = 5  # Number of columns
        self.max_width = 550  # Maximum width for items

        self.master.title("Media Viewer")
        self.master.configure(bg='black')

        self.load_media()
        self.setup_waterfall()

        # Resize the window to fit all items
        self.resize_window()

        # Move and resize the window
        self.master.geometry("1670x957+117+29")

    def load_media(self):
        media_extensions = ('.mp4', '.flv', '.mkv', '.m2ts', '.wemp',
                            '.mp3', '.wav', '.m4a', '.aac')

        self.media_files = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path)
                            if os.path.isfile(os.path.join(self.folder_path, f))
                            and f.lower().endswith(media_extensions)]

    def setup_waterfall(self):
        for idx, media_file in enumerate(self.media_files):
            label = tk.Label(self.master, text=os.path.basename(media_file), fg='white', bg='black', cursor='hand2')
            label.grid(row=self.current_row, column=idx % self.columns, padx=self.padding, pady=self.padding)
            label.bind("<Button-1>", lambda event, file=media_file: self.open_media(file))
            self.media_labels.append(label)

            # Move to the next row if necessary
            if idx % self.columns == self.columns - 1:
                self.current_row += 1

    def open_media(self, file):
        try:
            subprocess.Popen([r"C:\Users\Administrator\Desktop\ffplayAI.bat", file], shell=True)
        except Exception as e:
            print(f"Error opening {file}: {e}")

    def resize_window(self):
        self.master.update_idletasks()
        self.master.minsize(self.master.winfo_width(), self.master.winfo_height())

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path>")
        return
    
    folder_path = sys.argv[1]
    root = tk.Tk()
    app = WaterfallViewer(root, folder_path)
    root.mainloop()

if __name__ == '__main__':
    main()
