import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk, ImageColor
from CanvasManager import CanvasManager
from SelectionManager import SelectionManager
from DrawingTools import DrawingTools
from HistoryManager import HistoryManager
from MenuBuilder import MenuBuilder

class MainPaint:
    def __init__(self, root):
        self.menu_builder = None
        self.menu = None
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
        self.menu_builder = MenuBuilder(self.root, self)
        self.menu = self.menu_builder.build_main_menu()

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
