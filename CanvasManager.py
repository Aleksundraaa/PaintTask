import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

class CanvasManager:
    def __init__(self, root, width, height, bg_color):
        self.width = width
        self.height = height
        self.bg_color = bg_color

        self.canvas = tk.Canvas(root, width=width, height=height, bg=bg_color)
        self.canvas.pack()

        self.image = Image.new("RGB", (width, height), bg_color)
        self.draw = ImageDraw.Draw(self.image)
        self.photo_image = None

    def update_canvas(self):
        self.canvas.delete("all")
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)

    def resize_canvas(self, width, height):
        old_image = self.image.copy()
        self.width = width
        self.height = height
        self.image = Image.new("RGB", (width, height), self.bg_color)
        self.image.paste(old_image, (0, 0))
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.config(width=width, height=height)
        self.update_canvas()