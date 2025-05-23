import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk, ImageColor

class SelectionManager:
    def __init__(self, canvas_manager):
        self.canvas_manager = canvas_manager
        self.rect = None
        self.start = None
        self.end = None
        self.active = False
        self.image = None
        self.offset = (0, 0)

    def start_selection(self, x, y):
        self.start = (x, y)
        self.rect = (x, y, x, y)
        self.active = True
        self.update_selection_display()

    def update_selection(self, x, y):
        if self.active and self.start:
            x1, y1 = self.start
            self.rect = (x1, y1, x, y)
            self.update_selection_display()

    def end_selection(self, x, y):
        if self.start:
            x1, y1 = self.start
            x2, y2 = x, y
            self.rect = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            self.update_selection_display()

    def update_selection_display(self):
        self.canvas_manager.update_canvas()
        if self.rect:
            x1, y1, x2, y2 = self.rect
            self.canvas_manager.canvas.create_rectangle(
                x1, y1, x2, y2, outline="red", dash=(4, 4), tags="selection")

    def cancel_selection(self):
        self.rect = None
        self.active = False
        self.canvas_manager.update_canvas()

    def get_selection_area(self):
        if self.rect:
            return (min(self.rect[0], self.rect[2]),
                    min(self.rect[1], self.rect[3]),
                    max(self.rect[0], self.rect[2]),
                    max(self.rect[1], self.rect[3]))
        return None


class DrawingTools:
    def __init__(self, canvas_manager):
        self.canvas_manager = canvas_manager
        self.current_tool = "brush"
        self.current_color = "black"
        self.current_size = 5
        self.last_x = None
        self.last_y = None
        self.start_x = None
        self.start_y = None

    def set_tool(self, tool):
        self.current_tool = tool

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


class HistoryManager:
    def __init__(self, canvas_manager):
        self.canvas_manager = canvas_manager
        self.history = []

    def save_state(self):
        state = self.canvas_manager.image.copy()
        self.history.append(state)

    def undo(self):
        if self.history:
            self.canvas_manager.image = self.history.pop()
            self.canvas_manager.draw = ImageDraw.Draw(self.canvas_manager.image)
            self.canvas_manager.update_canvas()


class MainPaint:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")

        self.canvas_manager = CanvasManager(root, 800, 600, "white")
        self.selection_manager = SelectionManager(self.canvas_manager)
        self.drawing_tools = DrawingTools(self.canvas_manager)
        self.history_manager = HistoryManager(self.canvas_manager)

        self.clipboard = None

        self.setup_menu()
        self.setup_bindings()

    def setup_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        self._setup_file_menu(menu)
        self._setup_selection_menu(menu)
        self._setup_size_menu(menu)
        self._setup_tools_menu(menu)
        self._setup_color_menu(menu)
        self._setup_geometry_menu(menu)
        self._setup_text_menu(menu)

    def _setup_file_menu(self, menu):
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить как...", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Закрыть", command=self.root.quit)
        file_menu.add_command(label="Размер холста", command=self.change_canvas_size)

    def _setup_selection_menu(self, menu):
        selection_menu = tk.Menu(menu)
        menu.add_cascade(label="Выделить", menu=selection_menu)
        selection_menu.add_command(label="Прямоугольное выделение",
                                   command=lambda: self.drawing_tools.set_tool("selection"))
        selection_menu.add_command(label="Залить выделение", command=self.fill_selection)
        selection_menu.add_command(label="Вырезать выделения", command=self.cut_selection)
        selection_menu.add_command(label="Отменить выделение", command=self.selection_manager.cancel_selection)

    def _setup_size_menu(self, menu):
        size_menu = tk.Menu(menu)
        menu.add_cascade(label="Размер", menu=size_menu)
        for size in [2, 5, 7, 9, 11, 15]:
            size_menu.add_command(label=str(size), command=lambda s=size: self.drawing_tools.set_size(s))
        size_menu.add_command(label="Свой размер", command=self.input_size)

    def _setup_tools_menu(self, menu):
        tools_menu = tk.Menu(menu)
        menu.add_cascade(label="Инструменты", menu=tools_menu)
        tools_menu.add_command(label="Кисть", command=lambda: self.drawing_tools.set_tool("brush"))
        tools_menu.add_command(label="Ластик", command=lambda: self.drawing_tools.set_tool("eraser"))
        tools_menu.add_command(label="Заливка", command=lambda: self.drawing_tools.set_tool("fill"))

    def _setup_color_menu(self, menu):
        colour_menu = tk.Menu(menu)
        menu.add_cascade(label="Цвет", menu=colour_menu)
        colour_menu.add_command(label="Выбор цвета", command=self.choose_color)

    def _setup_geometry_menu(self, menu):
        geometry_menu = tk.Menu(menu)
        menu.add_cascade(label="Геометрическая фигура", menu=geometry_menu)
        geometry_menu.add_command(label="Круг", command=lambda: self.drawing_tools.set_tool("circle"))
        geometry_menu.add_command(label="Прямоугольник", command=lambda: self.drawing_tools.set_tool("rectangle"))
        geometry_menu.add_command(label="Прямая линия", command=lambda: self.drawing_tools.set_tool("straight_line"))
        geometry_menu.add_command(label="Эллипс", command=lambda: self.drawing_tools.set_tool("ellipse"))

    def _setup_text_menu(self, menu):
        text_menu = tk.Menu(menu)
        menu.add_cascade(label="Текст", menu=text_menu)
        text_menu.add_command(label="Добавить текст")

    def setup_bindings(self):
        self.canvas_manager.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas_manager.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas_manager.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Control-z>", self.undo)
        self.root.bind("<Control-s>", self.save_image)
        self.root.bind("<Control-x>", lambda e: self.cut_selection())

    def on_button_press(self, event):
        self.history_manager.save_state()

        if self.drawing_tools.current_tool == "selection":
            self.selection_manager.start_selection(event.x, event.y)
        else:
            self.drawing_tools.on_button_press(event.x, event.y)

    def on_mouse_drag(self, event):
        if self.drawing_tools.current_tool == "selection":
            self.selection_manager.update_selection(event.x, event.y)
        else:
            self.drawing_tools.on_mouse_drag(event.x, event.y)

    def on_button_release(self, event):
        if self.drawing_tools.current_tool == "selection":
            self.selection_manager.end_selection(event.x, event.y)
        else:
            self.drawing_tools.on_button_release(event.x, event.y)

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("BMP files", "*.bmp")])
        if file_path:
            self.canvas_manager.image.save(file_path)
            messagebox.showinfo("Сохранение...", "Сохранено!")

    def change_canvas_size(self):
        width = simpledialog.askinteger("Ширина холста", "Введите ширину", minvalue=100, maxvalue=2000)
        height = simpledialog.askinteger("Высота холста", "Введите высоту", minvalue=100, maxvalue=2000)
        if width and height:
            self.canvas_manager.resize_canvas(width, height)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.drawing_tools.set_color(color)

    def input_size(self):
        size = simpledialog.askinteger("Размер кисти", "Введите размер", minvalue=1, maxvalue=100)
        if size:
            self.drawing_tools.set_size(size)

    def fill_selection(self):
        if self.selection_manager.rect:
            self.history_manager.save_state()
            x1, y1, x2, y2 = self.selection_manager.get_selection_area()
            temp_image = Image.new("RGB", (abs(x2 - x1), abs(y2 - y1)), self.drawing_tools.current_color)
            self.canvas_manager.image.paste(temp_image, (min(x1, x2), min(y1, y2)))
            self.canvas_manager.draw = ImageDraw.Draw(self.canvas_manager.image)
            self.canvas_manager.update_canvas()
            self.selection_manager.cancel_selection()

    def cut_selection(self):
        if self.selection_manager.rect:
            self.history_manager.save_state()
            x1, y1, x2, y2 = self.selection_manager.get_selection_area()
            self.clipboard = self.canvas_manager.image.crop((x1, y1, x2, y2))
            self.canvas_manager.draw.rectangle(
                [x1, y1, x2, y2],
                fill=self.canvas_manager.bg_color,
                outline=self.canvas_manager.bg_color)
            self.canvas_manager.update_canvas()
            self.selection_manager.cancel_selection()

    def undo(self, event=None):
        self.history_manager.undo()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainPaint(root)
    root.mainloop()
