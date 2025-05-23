import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, simpledialog
from PIL import Image, ImageDraw, ImageTk, ImageColor


class MainPaint:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")

        self.selection_rect = None
        self.selection_start = None
        self.selection_end = None
        self.selection_active = False
        self.selection_image = None
        self.selection_offset = (0, 0)

        self.last_x = None
        self.last_y = None
        self.start_x = None
        self.start_y = None

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
        file_menu.add_command(label="Размер холста", command=self.change_canvas_size)

        selection_menu = tk.Menu(menu)
        menu.add_cascade(label="Выделить", menu=selection_menu)
        selection_menu.add_command(label="Прямоугольное выделение", command=lambda: self.select_tool("selection"))
        selection_menu.add_command(label = "Залить выделение", command=self.fill_selection)
        selection_menu.add_command(label="Удалить выделение", command=self.cancel_selection)

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

        geometry_menu = tk.Menu(menu)
        menu.add_cascade(label="Геометрическая фигура", menu=geometry_menu)
        geometry_menu.add_command(label="Круг", command=lambda: self.select_tool("circle"))
        geometry_menu.add_command(label="Прямоугольник", command=lambda: self.select_tool("rectangle"))
        geometry_menu.add_command(label="Прямая линия", command=lambda: self.select_tool("straight_line"))
        geometry_menu.add_command(label="Эллипс", command=lambda: self.select_tool("ellipse"))

        text_menu = tk.Menu(menu)
        menu.add_cascade(label="Текст", menu=text_menu)
        text_menu.add_command(label="Добавить текст")

    def save_image(self, event=None):
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
        if size:
            self.set_size(size)

    def change_canvas_size(self):
        width = simpledialog.askinteger("Ширина холста", "Введите ширину", minvalue=100, maxvalue=2000)
        height = simpledialog.askinteger("Высота холста", "Введите высоту", minvalue=100, maxvalue=2000)
        if width and height:
            self.canvas_width = width
            self.canvas_height = height
            self.update_canvas_size()

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.current_colour = color

    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Control-z>", self.remove_last_action)
        self.root.bind("<Control-s>", self.save_image)

    def remove_last_action(self, event=None):
        if len(self.history) > 0:
            self.image = self.history.pop()
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()

    def update_canvas(self):
        self.canvas.delete("all")
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)

        if self.selection_image and self.selection_offset:
            x1, y1, x2, y2 = self.selection_rect
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", dash=(4, 4), tags="selection")


    def update_canvas_size(self):
        old_image = self.image.copy()
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), self.background_colour)
        self.image.paste(old_image, (0, 0))
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.config(width=self.canvas_width, height=self.canvas_height)
        self.update_canvas()

    def select_tool(self, tool):
        if self.current_tool=="selection" and tool!="selection":
            self.cancel_selection()
        self.current_tool = tool

    def cancel_selection(self):
        self.selection_rect = None
        self.selection_active = False
        self.update_canvas()

    def fill_selection(self):
        if self.selection_rect:
            self.save_state()
            x1, y1, x2, y2 = self.selection_rect
            temp_image = Image.new("RGB", (abs(x2-x1), abs(y2-y1)), self.current_colour)
            self.image.paste(temp_image, (min(x1, x2), min(y1, y2)))
            self.draw = ImageDraw.Draw(self.image)
            self.update_canvas()
            self.cancel_selection()

    def save_state(self):
        state = self.image.copy()
        self.history.append(state)

    def on_button_press(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.last_x, self.last_y = event.x, event.y

        if self.current_tool == "selection":
            self.selection_start = (event.x, event.y)
            self.selection_rect = (event.x, event.y, event.x, event.y)



        if self.current_tool == "fill":
            self.save_state()
            fill_color = ImageColor.getrgb(self.current_colour)
            ImageDraw.floodfill(self.image, (event.x, event.y), fill_color)
            self.update_canvas()
        else:
            self.save_state()

    def on_button_release(self, event):
        if self.current_tool == "circle":
            self.canvas.delete("temp_circle")
            radius = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5
            self.draw.ellipse([self.start_x - radius, self.start_y - radius,
                               self.start_x + radius, self.start_y + radius],
                              outline=self.current_colour, width=self.current_size)
            self.update_canvas()

        elif self.current_tool == "rectangle":
            self.canvas.delete("temp_rectangle")
            self.draw.rectangle([self.start_x, self.start_y, event.x, event.y],
                                outline=self.current_colour, width=self.current_size)
            self.update_canvas()

        elif self.current_tool == "straight_line":
            self.canvas.delete("temp_line")
            self.draw.line([self.start_x, self.start_y, event.x, event.y], fill=self.current_colour,
                           width=self.current_size)
            self.update_canvas()


        elif self.current_tool == "ellipse":
            self.canvas.delete("temp_shape")
            self.draw.ellipse([self.start_x, self.start_y, event.x, event.y],
                              outline=self.current_colour, width=self.current_size)
            self.update_canvas()

        elif self.current_tool == "selection":
            self.selection_end = (event.x, event.y)
            x1, y1 = self.selection_start
            x2, y2 = self.selection_end
            self.selection_rect = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

    def on_mouse_drag(self, event):
        if self.current_tool in ["brush", "eraser"]:
            if self.current_tool == "brush":
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        fill=self.current_colour, width=self.current_size)
                self.draw.line([self.last_x, self.last_y, event.x, event.y],
                               fill=self.current_colour, width=self.current_size)
            elif self.current_tool == "eraser":
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        fill=self.background_colour, width=self.current_size)
                self.draw.line([self.last_x, self.last_y, event.x, event.y],
                               fill=self.background_colour, width=self.current_size)

            self.last_x, self.last_y = event.x, event.y
            self.update_canvas()

        elif self.current_tool == "circle":
            self.canvas.delete("temp_circle")
            radius = ((event.x - self.start_x) ** 2 + (event.y - self.start_y) ** 2) ** 0.5
            self.canvas.create_oval(self.start_x - radius, self.start_y - radius,
                                    self.start_x + radius, self.start_y + radius,
                                    outline=self.current_colour, width=self.current_size, tags="temp_circle")

        elif self.current_tool == "rectangle":
            self.canvas.delete("temp_rectangle")
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.current_colour,
                                         width=self.current_size, tags="temp_rectangle")

        elif self.current_tool == "straight_line":
            self.canvas.delete("temp_line")
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                    fill=self.current_colour, width=self.current_size,
                                    tags="temp_line")

        elif self.current_tool == "ellipse":
            self.canvas.delete("temp_ellipse")
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y,
                                    outline=self.current_colour, width=self.current_size, tags="temp_ellipse")

        elif self.current_tool == "selection" and self.selection_active:
            x1, y1 = self.selection_start
            self.selection_rect = (x1, y1, event.x, event.y)
            self.update_canvas()



if __name__ == "__main__":
    root = tk.Tk()
    app = MainPaint(root)
    root.mainloop()
