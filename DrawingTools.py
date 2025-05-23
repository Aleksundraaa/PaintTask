from PIL import ImageDraw, ImageColor

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

