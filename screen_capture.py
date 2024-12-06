import cv2
import mss
import numpy as np
import pygetwindow as gw


class ScreenCapture:
    def __init__(self, window_title="SM-G781B"):
        self.window_title = window_title
        self.scrcpy_window = None
        self.region = None
        self._find_window()
        self._calculate_region()

    def _find_window(self):
        for window in gw.getWindowsWithTitle(self.window_title):
            self.scrcpy_window = window
            break
        if self.scrcpy_window is None:
            raise RuntimeError(f"{self.window_title} window not found!")

    def _calculate_region(self):
        self.region = {
            "left": self.scrcpy_window.left + 10,
            "top": self.scrcpy_window.top + self.scrcpy_window.height // 2,
            "width": self.scrcpy_window.width - 20,
            "height": self.scrcpy_window.height // 2 - 10,
        }

    def capture(self):
        with mss.mss() as sct:
            screenshot = sct.grab(self.region)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        return frame
