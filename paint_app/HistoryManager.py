class HistoryManager:
    def __init__(self, canvas_manager, max_history=50):
        self.canvas_manager = canvas_manager
        self.history = []
        self.max_history = max_history

    def save_state(self):
        state = [layer.copy() for layer in self.canvas_manager.layers]
        self.history.append(state)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def undo(self):
        if self.history:
            previous_state = self.history.pop()
            self.canvas_manager.layers = [layer.copy() for layer in previous_state]

            self.canvas_manager.update_draw()
            self.canvas_manager.update_canvas()
