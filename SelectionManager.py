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