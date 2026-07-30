import ctypes
import datetime
import threading
import time

import pyautogui
import pystray
from PIL import Image, ImageDraw

INTERVAL_SECONDS = 60
SHUTDOWN_HOUR = 18  # 6pm

ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002

pyautogui.FAILSAFE = False

active = True
stop_event = threading.Event()
icon = None


def set_awake(awake: bool):
    if awake:
        ctypes.windll.kernel32.SetThreadExecutionState(
            ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED
        )
    else:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)


def create_icon(color):
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([8, 8, 56, 56], fill=color)
    return img


def jiggle_loop():
    while True:
        if stop_event.wait(INTERVAL_SECONDS):
            break
        if active:
            pyautogui.moveRel(1, 0, duration=0.1)
            time.sleep(0.1)
            pyautogui.moveRel(-1, 0, duration=0.1)


def auto_shutdown_loop():
    now = datetime.datetime.now()
    target = now.replace(hour=SHUTDOWN_HOUR, minute=0, second=0, microsecond=0)
    if now >= target:
        target += datetime.timedelta(days=1)
    wait_seconds = (target - now).total_seconds()
    if not stop_event.wait(wait_seconds):
        set_awake(False)
        stop_event.set()
        if icon:
            icon.stop()


def toggle(icon_ref, item):
    global active
    active = not active
    set_awake(active)
    icon_ref.icon = create_icon((46, 204, 113) if active else (231, 76, 60))
    icon_ref.title = f"Teams Jiggler — {'Activo' if active else 'Pausado'}"


def quit_app(icon_ref, item):
    set_awake(False)
    stop_event.set()
    icon_ref.stop()


set_awake(True)

threading.Thread(target=jiggle_loop, daemon=True).start()
threading.Thread(target=auto_shutdown_loop, daemon=True).start()

icon = pystray.Icon("teams_jiggler")
icon.icon = create_icon((46, 204, 113))
icon.title = "Teams Jiggler — Activo (se apaga a las 18:00)"
icon.menu = pystray.Menu(
    pystray.MenuItem("Activar / Pausar", toggle),
    pystray.MenuItem("Salir", quit_app),
)
icon.run()
