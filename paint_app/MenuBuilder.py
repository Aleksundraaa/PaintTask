import tkinter as tk
from random import gauss

from PIL import ImageFilter


class MenuBuilder:
    def __init__(self, root, app):
        self.root = root
        self.app = app

    def build_main_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        self._setup_file_menu(menu)
        self._setup_selection_menu(menu)
        self._setup_size_menu(menu)
        self._setup_tools_menu(menu)
        self._setup_color_menu(menu)
        self._setup_geometry_menu(menu)
        self._setup_text_menu(menu)

        return menu

    def _setup_file_menu(self, menu):
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить как...", command=self.app.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Закрыть", command=self.app.root.quit)
        file_menu.add_command(label="Размер холста", command=self.app.change_canvas_size)

    def _setup_selection_menu(self, menu):
        selection_menu = tk.Menu(menu)
        menu.add_cascade(label="Выделить", menu=selection_menu)
        selection_menu.add_command(label="Прямоугольное выделение",
                                   command=lambda: self.app.drawing_tools.set_tool("selection"))
        selection_menu.add_command(label="Залить выделение", command=self.app.fill_selection)
        selection_menu.add_command(label="Вырезать выделения", command=self.app.cut_selection)
        selection_menu.add_command(label="Отменить выделение", command=self.app.selection_manager.cancel_selection)

    def _setup_size_menu(self, menu):
        size_menu = tk.Menu(menu)
        menu.add_cascade(label="Размер", menu=size_menu)
        for size in [2, 5, 7, 9, 11, 15]:
            size_menu.add_command(label=str(size), command=lambda s=size: self.app.drawing_tools.set_size(s))
        size_menu.add_command(label="Свой размер", command=self.app.input_size)

    def _setup_tools_menu(self, menu):
        tools_menu = tk.Menu(menu)
        menu.add_cascade(label="Инструменты", menu=tools_menu)
        tools_menu.add_command(label="Кисть", command=lambda: self.app.drawing_tools.set_tool("brush"))
        tools_menu.add_command(label="Ластик", command=lambda: self.app.drawing_tools.set_tool("eraser"))
        tools_menu.add_command(label="Заливка", command=lambda: self.app.drawing_tools.set_tool("fill"))
        tools_menu.add_command(label="Перевод в чб", command=lambda: self.app.drawing_tools.set_tool("grayscale"))
        blur_menu = tk.Menu(menu)
        tools_menu.add_cascade(label="Размытие", menu=blur_menu)
        blur_menu.add_command(label="Размытие по Гауссу", command=lambda: self.app.drawing_tools.set_tool("gauss"))

    def _setup_color_menu(self, menu):
        colour_menu = tk.Menu(menu)
        menu.add_cascade(label="Цвет", menu=colour_menu)
        colour_menu.add_command(label="Выбор цвета", command=self.app.choose_color)

    def _setup_geometry_menu(self, menu):
        geometry_menu = tk.Menu(menu)
        menu.add_cascade(label="Геометрическая фигура", menu=geometry_menu)
        geometry_menu.add_command(label="Круг", command=lambda: self.app.drawing_tools.set_tool("circle"))
        geometry_menu.add_command(label="Прямоугольник", command=lambda: self.app.drawing_tools.set_tool("rectangle"))
        geometry_menu.add_command(label="Прямая линия",
                                  command=lambda: self.app.drawing_tools.set_tool("straight_line"))
        geometry_menu.add_command(label="Эллипс", command=lambda: self.app.drawing_tools.set_tool("ellipse"))

    def _setup_text_menu(self, menu):
        text_menu = tk.Menu(menu)
        menu.add_cascade(label="Текст", menu=text_menu)
        text_menu.add_command(label="Добавить текст", command=lambda: self.app.add_text())
