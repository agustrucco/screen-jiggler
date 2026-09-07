# Screen Jiggler

A personal Windows utility that keeps your screen on and prevents the PC from sleeping during long-running tasks — built to use alongside [Claude Code](https://claude.ai/code) or any other process that runs unattended for extended periods.

## The problem

Windows locks the screen and suspends the session after a few minutes of inactivity. When you run a long Claude Code task and step away, the session can freeze or lose context because the screen locks mid-run. This tool prevents that.

## How it works

Two mechanisms run in parallel:

1. **Windows API**: calls `SetThreadExecutionState` with `ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED` — the proper OS-level signal that tells Windows "do not sleep, do not dim the screen"
2. **Mouse nudge**: moves the cursor 1px right and back every 60 seconds as a belt-and-suspenders fallback for apps that ignore the API signal

The tool lives in the system tray. A green circle means it is active; red means it is paused. It auto-stops at 6:00 PM.

## Usage

```bash
pip install -r requirements.txt
python jiggler.py
```

The app runs silently in the system tray. Right-click the icon to toggle or quit.

## Build as a standalone exe

Requires [PyInstaller](https://pyinstaller.org/):

```bash
pip install pyinstaller
pyinstaller ScreenJiggler.spec
```

The compiled `ScreenJiggler.exe` will appear in `dist/`. No Python installation needed to run it.

## System tray controls

| Action | Effect |
|---|---|
| Toggle | Switch between Active (green) and Paused (red) |
| Quit | Restore normal sleep behavior and exit |

Auto-stop time is set via `SHUTDOWN_HOUR` in `jiggler.py` (default: 18, i.e. 6 PM).

## Requirements

- Windows (uses `ctypes.windll.kernel32`)
- Python 3.x
- `pyautogui`, `pystray`, `Pillow`