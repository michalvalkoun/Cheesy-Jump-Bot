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
            "top": self.scrcpy_window.top + 90,
            "width": self.scrcpy_window.width - 20,
            "height": self.scrcpy_window.height - 100,
        }

    def capture(self, resize_factor=0.5):
        with mss.mss() as sct:
            screenshot = sct.grab(self.region)
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Resize the frame to a lower resolution
            frame = cv2.resize(frame, None, fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_LINEAR)

        return frame

    def save_frame(self, frame, filename="screenshot.png"):
        try:
            cv2.imwrite(filename, frame)
            print(f"Frame saved successfully as {filename}")
        except Exception as e:
            print(f"Failed to save frame: {e}")
