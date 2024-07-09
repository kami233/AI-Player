import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import subprocess

class WaterfallViewer:
    def __init__(self, master, folder_path):
        self.master = master
        self.folder_path = folder_path
        self.images = []
        self.image_labels = []
        self.padding = 10  # Padding between images
        self.current_row = 0
        self.columns = 6  # Number of columns
        self.max_width = 270  # Maximum width for images

        self.master.title("Waterfall Viewer")
        self.master.configure(bg='black')

        self.load_images()
        self.setup_waterfall()

        # Resize the window to fit all images
        self.resize_window()

        # Move and resize the window (117, 29, 1670, 957)
        self.master.geometry("1670x957+117+29")

    def load_images(self):
        image_files = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path)
                       if os.path.isfile(os.path.join(self.folder_path, f))
                       and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        for image_file in image_files:
            try:
                img = Image.open(image_file)
                # Resize the image to fit within max_width while maintaining aspect ratio
                width_percent = self.max_width / float(img.size[0])
                new_height = int(float(img.size[1]) * float(width_percent))
                img = img.resize((self.max_width, new_height), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                self.images.append((img_tk, image_file, img.width, img.height))
            except Exception as e:
                print(f"Unable to process {image_file}: {e}")

    def setup_waterfall(self):
        self.column_widths = [0] * self.columns
        self.column_heights = [0] * self.columns

        for img_tk, image_file, img_width, img_height in self.images:
            column = self.get_shortest_column(self.column_heights)
            x = column * (self.column_width(self.column_widths) + self.padding)
            y = self.column_heights[column]

            label = tk.Label(self.master, image=img_tk, bg='black')
            label.image = img_tk  # Keep a reference to the image to prevent garbage collection
            label.place(x=x, y=y, width=img_width, height=img_height)

            label.bind('<Button-1>', lambda event, image_file=image_file: self.show_full_image(image_file))

            self.image_labels.append(label)
            self.column_heights[column] += img_height + self.padding
            self.column_widths[column] = max(self.column_widths[column], img_width)

    def get_shortest_column(self, column_heights):
        return min(range(len(column_heights)), key=column_heights.__getitem__)

    def column_width(self, column_widths):
        return max(column_widths) if any(column_widths) else 0

    def resize_window(self):
        max_height = max(self.column_heights) if any(self.column_heights) else 0  # Find the tallest column's height
        total_width = sum(self.column_widths) + (self.columns - 1) * self.padding  # Total width of all columns
        self.master.geometry(f"{total_width}x{max_height}")  # Set window size

    def show_full_image(self, image_file):
        command = [r"C:\Users\Administrator\Desktop\ffplayAI.bat", image_file]

        try:
            subprocess.Popen(command, shell=True)
        except Exception as e:
            print(f"Error executing script: {e}")

# def main():
    # folder_path = r"C:\Users\Administrator\Desktop\KuukoW"
    # root = tk.Tk()
    # app = WaterfallViewer(root, folder_path)
    # root.mainloop()
    
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