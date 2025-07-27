from PIL import ImageDraw, ImageColor, ImageFont, Image
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

        active_layer = self.canvas_manager.layers[self.canvas_manager.active_layer_index]

        if self.current_tool == "fill":
            fill_color = ImageColor.getrgb(self.current_color)
            try:
                ImageDraw.floodfill(active_layer, (x, y), fill_color)
            except Exception:
                print("Ошибка")
            self.canvas_manager.update_canvas()

        elif self.current_tool == "text" and not self.text_active:
            self.start_text_input(x, y)
            self.text_active = True

        elif self.text_active:
            self.finish_text_input()

    def apply_gaussian_blur_at(self, x, y, radius=1, region_size=40):
        active_layer = self.canvas_manager.layers[self.canvas_manager.active_layer_index]

        left = max(x - region_size // 2, 0)
        right = min(x + region_size // 2, active_layer.width)
        upper = max(y - region_size // 2, 0)
        lower = min(y + region_size // 2, active_layer.height)

        if left >= right or upper >= lower:
            return

        region = active_layer.crop((left, upper, right, lower)).convert("RGB")
        pixels = region.load()
        width, height = region.size
        result = Image.new("RGB", (width, height))
        result_pixels = result.load()

        for i in range(width):
            for j in range(height):
                r_sum, g_sum, b_sum = 0, 0, 0
                count = 0

                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < width and 0 <= ny < height:
                            pr, pg, pb = pixels[nx, ny]
                            r_sum += pr
                            g_sum += pg
                            b_sum += pb
                            count += 1

                r_avg = int(r_sum / count)
                g_avg = int(g_sum / count)
                b_avg = int(b_sum / count)

                result_pixels[i, j] = (r_avg, g_avg, b_avg)

        active_layer.paste(result, (left, upper))
        self.canvas_manager.update_canvas()

    def apply_grayscale_at(self, x, y, region_size=40):
        active_layer = self.canvas_manager.layers[self.canvas_manager.active_layer_index]

        left = max(x - region_size // 2, 0)
        right = min(x + region_size // 2, active_layer.width)
        upper = max(y - region_size // 2, 0)
        lower = min(y + region_size // 2, active_layer.height)

        if left >= right or upper >= lower:
            return

        region = active_layer.crop((left, upper, right, lower))
        pixels = region.load()

        for i in range(region.width):
            for j in range(region.height):
                pixel = pixels[i, j]
                r, g, b = pixel[:3]  # Берём первые три канала
                a = pixel[3] if len(pixel) == 4 else 255  # Альфа, если есть

                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                pixels[i, j] = (gray, gray, gray, a)

        active_layer.paste(region, (left, upper))
        self.canvas_manager.update_canvas()

    def apply_sharpen_at(self, x, y, region_size=40):
        active_layer = self.canvas_manager.layers[self.canvas_manager.active_layer_index]

        left = max(x - region_size // 2, 0)
        right = min(x + region_size // 2, active_layer.width)
        upper = max(y - region_size // 2, 0)
        lower = min(y + region_size // 2, active_layer.height)

        if left >= right or upper >= lower:
            return

        region = active_layer.crop((left, upper, right, lower)).convert("RGB")
        pixels = region.load()

        width, height = region.size
        result = Image.new("RGB", (width, height))
        result_pixels = result.load()

        amount = 1.5
        for i in range(width):
            for j in range(height):
                r, g, b = pixels[i, j]

                neighbors = []
                if i > 0:
                    neighbors.append(pixels[i - 1, j])
                if i < width - 1:
                    neighbors.append(pixels[i + 1, j])
                if j > 0:
                    neighbors.append(pixels[i, j - 1])
                if j < height - 1:
                    neighbors.append(pixels[i, j + 1])

                if neighbors:
                    nr = sum(n[0] for n in neighbors) / len(neighbors)
                    ng = sum(n[1] for n in neighbors) / len(neighbors)
                    nb = sum(n[2] for n in neighbors) / len(neighbors)
                else:
                    nr, ng, nb = r, g, b

                sr = int(r + amount * (r - nr))
                sg = int(g + amount * (g - ng))
                sb = int(b + amount * (b - nb))

                sr = max(0, min(255, sr))
                sg = max(0, min(255, sg))
                sb = max(0, min(255, sb))

                result_pixels[i, j] = (sr, sg, sb)

        active_layer.paste(result, (left, upper))
        self.canvas_manager.update_canvas()

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
                except Exception:
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
        active_layer = self.canvas_manager.layers[self.canvas_manager.active_layer_index]

        if self.current_tool in ["brush", "eraser"]:
            color = self.current_color if self.current_tool == "brush" else (0, 0, 0, 0)
            self.canvas_manager.draw.line(
                [self.last_x, self.last_y, x, y], fill=color, width=self.current_size)
            self.last_x, self.last_y = x, y
            self.canvas_manager.update_canvas()

        elif self.current_tool in ["circle", "rectangle", "straight_line", "ellipse"]:
            self.draw_temp_shape(x, y)

        elif self.current_tool == "gauss":
            self.apply_gaussian_blur_at(x, y, self.current_size)

        elif self.current_tool == "grayscale":
            self.apply_grayscale_at(x, y, self.current_size)

        elif self.current_tool == "sharpen":
            self.apply_sharpen_at(x, y, self.current_size)

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
        self.canvas_manager.canvas.delete("temp_shape")

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
