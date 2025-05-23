from PIL import ImageDraw


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