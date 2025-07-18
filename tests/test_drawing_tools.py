import pytest
from unittest.mock import Mock, MagicMock
from paint_app.DrawingTools import DrawingTools
from PIL import Image, ImageDraw

@pytest.fixture
def mock_canvas_manager():
    image = Image.new("RGB", (100, 100), "white")
    canvas_manager = Mock()
    canvas_manager.image = image
    canvas_manager.bg_color = "white"
    canvas_manager.draw = ImageDraw.Draw(image)
    canvas_manager.update_canvas = MagicMock()
    canvas_manager.canvas = Mock()
    return canvas_manager

def test_set_tool(mock_canvas_manager):
    drawing_tools = DrawingTools(mock_canvas_manager)
    drawing_tools.set_tool("eraser")
    assert drawing_tools.current_tool == "eraser"

def test_set_color(mock_canvas_manager):
    drawing_tools = DrawingTools(mock_canvas_manager)
    drawing_tools.set_color("red")
    assert drawing_tools.current_color == "red"

def test_set_size(mock_canvas_manager):
    drawing_tools = DrawingTools(mock_canvas_manager)
    drawing_tools.set_size(10)
    assert drawing_tools.current_size == 10

