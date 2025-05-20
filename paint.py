import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageDraw


class MainPaint:

    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")
        self.last_x = None
        self.last_y = None

        self.canvas_width = 800
        self.canvas_height = 600
        self.background_colour = "white"

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg=self.background_colour)
        self.canvas.pack()

        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.background_colour)
        self.draw = ImageDraw.Draw(self.image)

        self.current_tool = "brush"
        self.current_colour = "black"

        self.setup_menu()
        self.setup_bindings()

    def setup_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить как...", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Закрыть", command=self.root.quit)

        tools_menu = tk.Menu(menu)
        menu.add_cascade(label="Инструменты", menu=tools_menu)
        menu.add_command(label="Кисть", command=lambda: self.select_tool("brush"))
        menu.add_command(label="Ластик", command=lambda: self.select_tool("eraser"))
        menu.add_command(label="Заливка", command=lambda: self.select_tool("fill"))

        colour_menu = tk.Menu(menu)
        menu.add_cascade(label="Цвет", menu=colour_menu)
        menu.add_command(label="Выбор цвета", command=self.choose_color)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("BMP files", "*.bmp")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Сохранение...", "Сохранено!")

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_colour = color

    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)

    def select_tool(self, tool):
        self.current_tool = tool

    def on_button_press(self, event):
        self.last_x, self.last_y = event.x, event.y

    def on_mouse_drag(self, event):
        if self.current_tool == "brush":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.current_colour, width=2)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.current_colour, width=2)
        elif self.current_tool == "eraser":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.background_colour, width=10)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.background_colour, width=10)
        elif self.current_tool == "fill":
            self.canvas.create_rectangle(event.x, event.y, event.x + 10, event.y + 10, fill=self.current_colour,
                                         outline=self.current_colour)
            self.draw.rectangle([event.x, event.y, event.x + 10, event.y + 10], fill=self.current_colour)

        self.last_x, self.last_y = event.x, event.y


if __name__ == "__main__":
    root = tk.Tk()
    app = MainPaint(root)
    root.mainloop()
