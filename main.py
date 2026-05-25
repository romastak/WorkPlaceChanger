import threading
import time
import keyboard
from pynput import mouse
import pystray
from PIL import Image, ImageDraw
import ctypes


EDGE_SIZE = 5          # размер зоны у края экрана
SCROLL_COOLDOWN = 0.15 # задержка между переключениями


user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)


last_trigger_time = 0


def switch_desktop(direction: str):
    """
    direction:
        left  -> предыдущий стол
        right -> следующий стол
    """

    if direction == "left":
        keyboard.press("ctrl+windows+left")
        keyboard.release("ctrl+windows+left")

    elif direction == "right":
        keyboard.press("ctrl+windows+right")
        keyboard.release("ctrl+windows+right")


def is_left_edge(x: int) -> bool:
    return x <= EDGE_SIZE


def is_right_edge(x: int) -> bool:
    return x >= SCREEN_WIDTH - EDGE_SIZE


def on_scroll(x, y, dx, dy):
    global last_trigger_time

    current_time = time.time()

    if current_time - last_trigger_time < SCROLL_COOLDOWN:
        return

    if is_left_edge(x):
        switch_desktop("left")
        last_trigger_time = current_time

    elif is_right_edge(x):
        switch_desktop("right")
        last_trigger_time = current_time


def create_image():
    image = Image.new("RGB", (64, 64), color=(30, 30, 30))
    draw = ImageDraw.Draw(image)

    draw.rectangle((16, 16, 48, 48), outline="white", width=3)

    return image


def quit_app(icon, item):
    icon.stop()


def start_mouse_listener():
    listener = mouse.Listener(
        on_scroll=on_scroll
    )

    listener.start()
    listener.join()


def main():
    mouse_thread = threading.Thread(
        target=start_mouse_listener,
        daemon=True
    )
    mouse_thread.start()

    icon = pystray.Icon(
        "WorkPlaceChanger",
        create_image(),
        "WorkPlaceChanger",
        menu=pystray.Menu(
            pystray.MenuItem("Exit", quit_app)
        )
    )

    icon.run()


if __name__ == "__main__":
    main()