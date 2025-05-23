from PIL import ImageTk, ImageDraw
import tkinter as tk


class SelectionManager:
    def __init__(self, canvas_manager):
        self.canvas_manager = canvas_manager
        self.rect = None
        self.start = None
        self.end = None
        self.active = False
        self.dragging = False
        self.selection_image = None
        self.offset = (0, 0)
        self.drag_start = None

    def start_selection(self, x, y):
        self.start = (x, y)
        self.rect = (x, y, x, y)
        self.active = True
        self.dragging = False
        self.update_selection_display()

    def update_selection(self, x, y):
        if not self.dragging and self.active and self.start:
            x1, y1 = self.start
            self.rect = (x1, y1, x, y)
            self.update_selection_display()
        elif self.dragging and self.rect:
            dx = x - self.drag_start[0]
            dy = y - self.drag_start[1]
            x1, y1, x2, y2 = self.rect
            self.rect = (x1 + dx, y1 + dy, x2 + dx, y2 + dy)
            self.drag_start = (x, y)
            self.update_selection_display()

    def end_selection(self, x, y):
        if self.start:
            x1, y1 = self.start
            x2, y2 = x, y
            self.rect = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
            self.active = False

            if not self.dragging:
                self._capture_selection()
            else:
                self._paste_selection()
                self.dragging = False

            self.update_selection_display()

    def _capture_selection(self):
        if self.rect:
            x1, y1, x2, y2 = self.get_selection_area()
            self.selection_image = self.canvas_manager.image.crop((x1, y1, x2, y2))
            self.offset = (x1, y1)

    def _paste_selection(self):
        if self.selection_image and self.rect:
            x1, y1, x2, y2 = self.rect
            self.canvas_manager.draw.rectangle(
                [x1, y1, x2, y2],
                fill=self.canvas_manager.bg_color,
                outline=self.canvas_manager.bg_color)
            self.canvas_manager.image.paste(self.selection_image, (x1, y1))
            self.canvas_manager.draw = ImageDraw.Draw(self.canvas_manager.image)
            self.offset = (x1, y1)

    def start_dragging(self, x, y):
        if self.rect and self.point_in_selection(x, y):
            self.dragging = True
            self.drag_start = (x, y)
            return True
        return False

    def point_in_selection(self, x, y):
        if not self.rect:
            return False
        x1, y1, x2, y2 = self.get_selection_area()
        return x1 <= x <= x2 and y1 <= y <= y2

    def update_selection_display(self):
        self.canvas_manager.update_canvas()
        if self.rect:
            x1, y1, x2, y2 = self.rect
            self.canvas_manager.canvas.create_rectangle(
                x1, y1, x2, y2, outline="red", dash=(4, 4), tags="selection")
            if self.selection_image and self.dragging:
                selection_photo = ImageTk.PhotoImage(self.selection_image)
                self.canvas_manager.canvas.create_image(
                    x1, y1, image=selection_photo, anchor=tk.NW, tags="selection_img")
                self.canvas_manager.canvas.selection_img = selection_photo

    def cancel_selection(self):
        self.rect = None
        self.active = False
        self.dragging = False
        self.selection_image = None
        self.canvas_manager.update_canvas()

    def get_selection_area(self):
        if self.rect:
            return (min(self.rect[0], self.rect[2]),
                    min(self.rect[1], self.rect[3]),
                    max(self.rect[0], self.rect[2]),
                    max(self.rect[1], self.rect[3]))
        return None
