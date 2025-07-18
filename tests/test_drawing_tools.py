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


def test_drawing_line(mock_canvas_manager):
    drawing_tools = DrawingTools(mock_canvas_manager)
    drawing_tools.set_tool("brush")
    drawing_tools.set_color("green")
    drawing_tools.set_size(5)

    drawing_tools.start_x, drawing_tools.start_y = 10, 10
    drawing_tools.draw_line(20, 20)

    pixels = [mock_canvas_manager.image.getpixel((x, x)) for x in range(10, 21)]
    assert any(p != (255, 255, 255) for p in pixels)


def test_eraser(mock_canvas_manager):
    drawing_tools = DrawingTools(mock_canvas_manager)
    drawing_tools.set_tool("brush")
    drawing_tools.set_color("green")
    drawing_tools.set_size(5)

    drawing_tools.start_x, drawing_tools.start_y = 10, 10
    drawing_tools.draw_line(20, 20)

    drawing_tools.set_tool("eraser")
    drawing_tools.start_x, drawing_tools.start_y = 10, 10
    drawing_tools.draw_line(20, 20)

    pixels = [mock_canvas_manager.image.getpixel((x, x)) for x in range(10, 21)]
    assert all(p == (255, 255, 255) for p in pixels)


def test_fill(mock_canvas_manager):
    drawing_tools = DrawingTools(mock_canvas_manager)
    drawing_tools.set_tool("fill")
    drawing_tools.set_color("blue")

    drawing_tools.on_button_press(50, 50)
    pixel = mock_canvas_manager.image.getpixel(50, 50)
    assert pixel == (0, 0, 255)


def test_gauss_blur(mock_canvas_manager):
    drawing_tools = DrawingTools(mock_canvas_manager)
    drawing_tools.set_tool("brush")
    drawing_tools.set_color("black")
    drawing_tools.set_size(5)

    drawing_tools.start_x, drawing_tools.start_y = 10, 10
    drawing_tools.draw_line(20, 20)

    before_blur_color = mock_canvas_manager.image.crop((45, 45, 55, 55)).getcolors()
    drawing_tools.set_tool("gauss")
    drawing_tools.on_mouse_drag(50, 50)
    after_blur_color = mock_canvas_manager.image.crop((45, 45, 55, 55)).getcolors()

    assert before_blur_color != after_blur_color


def test_on_button_release(mock_canvas_manager):
    tools = DrawingTools(mock_canvas_manager)
    tools.last_x = 10
    tools.last_y = 20
    tools.on_button_release(30, 40)
    assert tools.last_x is None
    assert tools.last_y is None
