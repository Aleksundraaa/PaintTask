from PIL import ImageDraw, ImageColor, ImageFont, ImageFilter
import tkinter as tk


class DrawingTools:
    def __init__(self, canvas_manager):
        self.canvas_manager = canvas_manager
        self.current_tool = "brush"
        self.current_color = "black"
        self.current_size = 5
        self.current_text_size = 12
        self.last_x = None
        self.last_y = None
        self.start_x = None
        self.start_y = None
        self.current_font = ImageFont.load_default()
        self.text_entry = None
        self.text_start_pos = None
        self.text_active = False

    def set_tool(self, tool):
        if self.text_entry:
            self.finish_text_input()
        self.current_tool = tool
        self.text_active = False

    def set_color(self, color):
        self.current_color = color

    def set_size(self, size):
        self.current_size = size

    def on_button_press(self, x, y):
        self.start_x, self.start_y = x, y
        self.last_x, self.last_y = x, y

        if self.current_tool == "fill":
            fill_color = ImageColor.getrgb(self.current_color)
            ImageDraw.floodfill(self.canvas_manager.image, (x, y), fill_color)
            self.canvas_manager.update_canvas()
        elif self.current_tool == "text" and not self.text_active:
            self.start_text_input(x, y)
            self.text_active = True

        elif self.text_active:
            self.finish_text_input()

    def apply_gaussian_blur_at(self, x, y, radius, region_size=40):
        left = max(x - region_size // 2, 0)
        right = min(x + region_size // 2, self.canvas_manager.image.width)
        upper = max(y - region_size // 2, 0)
        lower = min(y + region_size // 2, self.canvas_manager.image.height)

        if left >= right or upper >= lower:
            return

        region = self.canvas_manager.image.crop((left, upper, right, lower))
        blurred_region = region.filter(ImageFilter.GaussianBlur(radius=radius))
        self.canvas_manager.image.paste(blurred_region, (left, upper))

    def apply_grayscale_at(self, x, y, radius, region_size=40):
        left = max(x - region_size // 2, 0)
        right = min(x + region_size // 2, self.canvas_manager.image.width)
        upper = max(y - region_size // 2, 0)
        lower = min(y + region_size // 2, self.canvas_manager.image.height)

        if left >= right or upper >= lower:
            return

        region = self.canvas_manager.image.crop((left, upper, right, lower))
        grayscale_region = region.convert("L").convert("RGB")
        self.canvas_manager.image.paste(grayscale_region, (left, upper))

    def start_text_input(self, x, y):
        self.text_start_pos = (x, y)

        self.text_entry = tk.Text(
            self.canvas_manager.canvas,
            width=30,
            height=1,
            font=("Arial", self.current_text_size),
            wrap=tk.WORD,
            bd=1,
            relief=tk.SOLID
        )

        self.canvas_manager.canvas.create_window(
            x, y,
            window=self.text_entry,
            anchor=tk.NW,
            tags="text_input"
        )

        self.text_entry.focus_set()

        self.text_entry.bind("<Return>", lambda e: self.finish_text_input())

    def finish_text_input(self, event=None):
        if self.text_entry and self.text_start_pos:
            text = self.text_entry.get("1.0", "end-1c")

            if text.strip():
                x, y = self.text_start_pos

                try:
                    font = ImageFont.truetype("arial.ttf", self.current_text_size)
                except:
                    font = ImageFont.load_default()

                self.canvas_manager.draw.text(
                    (x, y),
                    text,
                    fill=self.current_color,
                    font=font
                )

                self.canvas_manager.update_canvas()

            self.text_entry.destroy()
            self.text_entry = None
            self.canvas_manager.canvas.delete("text_input")
            self.text_start_pos = None
            self.text_active = False

    def on_mouse_drag(self, x, y):
        if self.current_tool in ["brush", "eraser"]:
            color = self.current_color if self.current_tool == "brush" else self.canvas_manager.bg_color
            self.canvas_manager.canvas.create_line(
                self.last_x, self.last_y, x, y, fill=color, width=self.current_size)
            self.canvas_manager.draw.line(
                [self.last_x, self.last_y, x, y], fill=color, width=self.current_size)
            self.last_x, self.last_y = x, y
            self.canvas_manager.update_canvas()

        elif self.current_tool in ["circle", "rectangle", "straight_line", "ellipse"]:
            self.draw_temp_shape(x, y)

        elif self.current_tool == "gauss":
            self.apply_gaussian_blur_at(x, y, self.current_size)
            self.canvas_manager.update_canvas()

        elif self.current_tool == "grayscale":
            self.apply_grayscale_at(x, y, self.current_size)
            self.canvas_manager.update_canvas()

    def on_button_release(self, x, y):
        if self.current_tool == "circle":
            self.draw_circle(x, y)
        elif self.current_tool == "rectangle":
            self.draw_rectangle(x, y)
        elif self.current_tool == "straight_line":
            self.draw_line(x, y)
        elif self.current_tool == "ellipse":
            self.draw_ellipse(x, y)

        self.canvas_manager.update_canvas()

    def draw_temp_shape(self, x, y):
        self.canvas_manager.canvas.delete("temp_shape")

        if self.current_tool == "circle":
            radius = ((x - self.start_x) ** 2 + (y - self.start_y) ** 2) ** 0.5
            self.canvas_manager.canvas.create_oval(
                self.start_x - radius, self.start_y - radius,
                self.start_x + radius, self.start_y + radius,
                outline=self.current_color, width=self.current_size, tags="temp_shape")

        elif self.current_tool == "rectangle":
            self.canvas_manager.canvas.create_rectangle(
                self.start_x, self.start_y, x, y,
                outline=self.current_color, width=self.current_size, tags="temp_shape")

        elif self.current_tool == "straight_line":
            self.canvas_manager.canvas.create_line(
                self.start_x, self.start_y, x, y,
                fill=self.current_color, width=self.current_size, tags="temp_shape")

        elif self.current_tool == "ellipse":
            self.canvas_manager.canvas.create_oval(
                self.start_x, self.start_y, x, y,
                outline=self.current_color, width=self.current_size, tags="temp_shape")

    def draw_circle(self, x, y):
        radius = ((x - self.start_x) ** 2 + (y - self.start_y) ** 2) ** 0.5
        self.canvas_manager.draw.ellipse([
            self.start_x - radius, self.start_y - radius,
            self.start_x + radius, self.start_y + radius],
            outline=self.current_color, width=self.current_size)

    def draw_rectangle(self, x, y):
        self.canvas_manager.draw.rectangle([
            self.start_x, self.start_y, x, y],
            outline=self.current_color, width=self.current_size)

    def draw_line(self, x, y):
        self.canvas_manager.draw.line([
            self.start_x, self.start_y, x, y],
            fill=self.current_color, width=self.current_size)

    def draw_ellipse(self, x, y):
        self.canvas_manager.draw.ellipse([
            self.start_x, self.start_y, x, y],
            outline=self.current_color, width=self.current_size)
