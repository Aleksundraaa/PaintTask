import tkinter as tk
from PIL import Image, ImageDraw, ImageTk, ImageColor


class CanvasManager:
    def __init__(self, root, width, height, bg_color):
        self.width = width
        self.height = height

        if isinstance(bg_color, str):
            rgba_color = ImageColor.getcolor(bg_color, "RGBA")
            hex_color = '#{:02x}{:02x}{:02x}'.format(*rgba_color[:3])
        elif isinstance(bg_color, tuple) and len(bg_color) >= 3:
            rgba_color = bg_color
            hex_color = '#{:02x}{:02x}{:02x}'.format(*bg_color[:3])
        else:
            raise ValueError("Неподдерживаемый формат цвета")

        self.bg_color = rgba_color
        self.tk_bg_color = hex_color
        self.canvas = tk.Canvas(root, width=width, height=height, bg=self.tk_bg_color)
        self.canvas.pack()

        base_layer = Image.new("RGBA", (width, height), self.bg_color)
        self.layers = [base_layer]
        self.active_layer_index = 0
        self.draw = ImageDraw.Draw(self.layers[self.active_layer_index])
        self.photo_image = None

    def get_composited_image(self):
        base = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        for layer in self.layers:
            base = Image.alpha_composite(base, layer)
        return base.convert("RGB")

    def update_canvas(self):
        self.canvas.delete("all")
        active_layer = self.layers[self.active_layer_index]
        background = Image.new("RGBA", (self.width, self.height), self.bg_color)
        combined = Image.alpha_composite(background, active_layer)
        image = combined.convert("RGB")

        self.photo_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)

    def update_draw(self):
        self.draw = ImageDraw.Draw(self.layers[self.active_layer_index])

    def switch_layer(self, index):
        if 0 <= index < len(self.layers):
            self.active_layer_index = index
            self.update_draw()
            self.update_canvas()

    def add_layer(self):
        new_layer = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.layers.append(new_layer)
        self.switch_layer(len(self.layers) - 1)
        self.update_canvas()

    def delete_layer(self, index):
        if 0 <= index < len(self.layers) and len(self.layers) > 1:
            del self.layers[index]
            self.active_layer_index = max(0, index - 1)
            self.update_draw()
            self.update_canvas()

    def resize_canvas(self, width, height):
        old_layers = self.layers.copy()
        self.width = width
        self.height = height
        self.layers = []

        for layer in old_layers:
            new_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            new_layer.paste(layer, (0, 0))
            self.layers.append(new_layer)

        self.switch_layer(min(self.active_layer_index, len(self.layers) - 1))
        self.canvas.config(width=width, height=height)
        self.update_canvas()
