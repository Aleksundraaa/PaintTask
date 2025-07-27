import tkinter as tk


class MenuBuilder:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.layer_menu = None
        self.select_submenu = None

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
        self._setup_layer_menu(menu)

        return menu

    def _setup_file_menu(self, menu):
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить как...", command=self.app.save_image)
        file_menu.add_separator()
        file_menu.add_command(label="Размер холста", command=self.app.change_canvas_size)
        file_menu.add_separator()
        file_menu.add_command(label="Закрыть", command=self.app.root.quit)

    def _setup_selection_menu(self, menu):
        selection_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Выделить", menu=selection_menu)
        selection_menu.add_command(label="Прямоугольное выделение",
                                   command=lambda: self.app.drawing_tools.set_tool("selection"))
        selection_menu.add_command(label="Залить выделение", command=self.app.fill_selection)
        selection_menu.add_command(label="Вырезать выделение", command=self.app.cut_selection)
        selection_menu.add_command(label="Отменить выделение", command=self.app.selection_manager.cancel_selection)

    def _setup_size_menu(self, menu):
        size_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Размер", menu=size_menu)
        for size in [2, 5, 7, 9, 11, 15]:
            size_menu.add_command(label=str(size), command=lambda s=size: self.app.drawing_tools.set_size(s))
        size_menu.add_command(label="Свой размер", command=self.app.input_size)

    def _setup_tools_menu(self, menu):
        tools_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Инструменты", menu=tools_menu)
        tools_menu.add_command(label="Кисть", command=lambda: self.app.drawing_tools.set_tool("brush"))
        tools_menu.add_command(label="Ластик", command=lambda: self.app.drawing_tools.set_tool("eraser"))
        tools_menu.add_command(label="Заливка", command=lambda: self.app.drawing_tools.set_tool("fill"))

        tools_menu.add_separator()
        tools_menu.add_command(label="Черно-белый", command=lambda: self.app.drawing_tools.set_tool("grayscale"))
        tools_menu.add_command(label="Повысить резкость", command=lambda: self.app.drawing_tools.set_tool("sharpen"))

        blur_menu = tk.Menu(tools_menu, tearoff=0)
        blur_menu.add_command(label="Гауссово размытие", command=lambda: self.app.drawing_tools.set_tool("gauss"))
        tools_menu.add_cascade(label="Размытие", menu=blur_menu)

    def _setup_color_menu(self, menu):
        colour_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Цвет", menu=colour_menu)
        colour_menu.add_command(label="Выбор цвета", command=self.app.choose_color)

    def _setup_geometry_menu(self, menu):
        geometry_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Фигуры", menu=geometry_menu)
        geometry_menu.add_command(label="Круг", command=lambda: self.app.drawing_tools.set_tool("circle"))
        geometry_menu.add_command(label="Прямоугольник", command=lambda: self.app.drawing_tools.set_tool("rectangle"))
        geometry_menu.add_command(label="Линия", command=lambda: self.app.drawing_tools.set_tool("straight_line"))
        geometry_menu.add_command(label="Эллипс", command=lambda: self.app.drawing_tools.set_tool("ellipse"))

    def _setup_text_menu(self, menu):
        text_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Текст", menu=text_menu)
        text_menu.add_command(label="Добавить текст", command=self.app.add_text)

    def _setup_layer_menu(self, menu):
        # Если меню уже есть — удаляем, чтобы пересоздать
        if self.layer_menu is not None:
            menu.delete("Слои")

        self.layer_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Слои", menu=self.layer_menu)

        self.layer_menu.add_command(label="Добавить слой", command=self._add_layer_and_refresh)
        self.layer_menu.add_command(label="Удалить активный слой",
                                    command=self._delete_layer_and_refresh)

        self.select_submenu = tk.Menu(self.layer_menu, tearoff=0)
        self._refresh_layer_selection_menu()
        self.layer_menu.add_cascade(label="Переключить слой", menu=self.select_submenu)

    def _refresh_layer_selection_menu(self):
        self.select_submenu.delete(0, tk.END)
        for i in range(len(self.app.canvas_manager.layers)):
            self.select_submenu.add_command(
                label=f"Слой {i + 1}",
                command=lambda index=i: self.app.canvas_manager.switch_layer(index)
            )

    def _add_layer_and_refresh(self):
        self.app.canvas_manager.add_layer()
        self._refresh_layer_selection_menu()
        self.app.canvas_manager.update_canvas()

    def _delete_layer_and_refresh(self):
        self.app.canvas_manager.delete_layer(self.app.canvas_manager.active_layer_index)
        self._refresh_layer_selection_menu()
        self.app.canvas_manager.update_canvas()
