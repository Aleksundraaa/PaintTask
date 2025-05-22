import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk, ImageColor


class MainPaint:

    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")
        self.last_x = None
        self.last_y = None

        self.photo_image = None

        self.canvas_width = 800
        self.canvas_height = 600
        self.background_colour = "white"

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg=self.background_colour)
        self.canvas.pack()

        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.background_colour)
        self.draw = ImageDraw.Draw(self.image)

        self.current_tool = "brush"
        self.current_colour = "black"

        self.history = []
        self.current_size = 5

        self.setup_menu()
        self.setup_bindings()

        self.update_canvas()

    def setup_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить как...", command=self.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Закрыть", command=self.root.quit)

        size_menu = tk.Menu(menu)
        menu.add_cascade(label="Размер", menu=size_menu)
        size_menu.add_command(label="2", command=lambda: self.set_size(2))
        size_menu.add_command(label="5", command=lambda: self.set_size(5))
        size_menu.add_command(label="7", command=lambda: self.set_size(7))
        size_menu.add_command(label="9", command=lambda: self.set_size(9))
        size_menu.add_command(label="11", command=lambda: self.set_size(11))
        size_menu.add_command(label="15", command=lambda: self.set_size(15))
        size_menu.add_command(label="Свой размер", command=lambda: self.input_size())

        tools_menu = tk.Menu(menu)
        menu.add_cascade(label="Инструменты", menu=tools_menu)
        tools_menu.add_command(label="Кисть", command=lambda: self.select_tool("brush"))
        tools_menu.add_command(label="Ластик", command=lambda: self.select_tool("eraser"))
        tools_menu.add_command(label="Заливка", command=lambda: self.select_tool("fill"))

        colour_menu = tk.Menu(menu)
        menu.add_cascade(label="Цвет", menu=colour_menu)
        colour_menu.add_command(label="Выбор цвета", command=self.choose_color)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg"),
                                                            ("BMP files", "*.bmp")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Сохранение...", "Сохранено!")

    def set_size(self, size):
        self.current_size = size

    def input_size(self):
        size = simpledialog.askinteger("Размер кисти", "Введите размер", minvalue=1, maxvalue=100)
        self.set_size(size)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_colour = color

    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.root.bind("<Control-z>", self.remove_last_action)

    def remove_last_action(self, event=None):
        if len(self.history) > 0:
            self.image = self.history.pop()
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)

    def select_tool(self, tool):
        self.current_tool = tool

    def save_state(self):
        state = self.image.copy()
        self.history.append(state)

    def on_button_press(self, event):
        self.last_x, self.last_y = event.x, event.y
        if self.current_tool == "fill":
            self.save_state()
            rgb_colour = ImageColor.getrgb(self.current_colour)
            ImageDraw.floodfill(self.image, (event.x, event.y), rgb_colour)
            self.update_canvas()
        else:
            self.save_state()

    def on_mouse_drag(self, event):
        if self.current_tool == "brush":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.current_colour,
                                    width=self.current_size)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.current_colour,
                           width=self.current_size)
        elif self.current_tool == "eraser":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill=self.background_colour,
                                    width=self.current_size)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.background_colour,
                           width=self.current_size)

        self.last_x, self.last_y = event.x, event.y
        self.update_canvas()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainPaint(root)
    root.mainloop()
