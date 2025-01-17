import time
from collections import deque

import cv2


class FPSCounter:
    def __init__(self, average_over=30):
        self.prev_time = time.time()
        self.current_fps = 0
        self.fps_values = deque(maxlen=average_over)

    def update(self):
        current_time = time.time()
        fps = 1 / (current_time - self.prev_time)
        self.prev_time = current_time

        self.fps_values.append(fps)
        self.current_fps = sum(self.fps_values) / len(self.fps_values)

    def get_fps(self):
        return self.current_fps

    def draw_fps(
        self, frame, position=(10, 30), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(0, 255, 0), thickness=2
    ):
        fps_text = f"FPS: {int(self.current_fps)}"
        cv2.putText(frame, fps_text, position, font, font_scale, color, thickness)
