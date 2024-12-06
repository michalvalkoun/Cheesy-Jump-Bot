import cv2
import numpy as np


class BallAndPlatformDetector:
    def __init__(self):
        self.platform_templates, self.ball_template = self.initialize_templates()

    def initialize_templates(self):
        """Load templates from image files."""
        platform_templates = [
            cv2.imread("images/platform_1.png", cv2.IMREAD_GRAYSCALE),
            cv2.imread("images/platform_2.png", cv2.IMREAD_GRAYSCALE),
            cv2.imread("images/platform_4.png", cv2.IMREAD_GRAYSCALE),
        ]
        ball_template = cv2.imread("images/cheese.png", cv2.IMREAD_GRAYSCALE)
        return platform_templates, ball_template

    def _detect_platforms(self, frame_gray):
        platforms = []
        for platform_template in self.platform_templates:
            result = cv2.matchTemplate(frame_gray, platform_template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            locations = np.where(result >= threshold)

            for pt in zip(*locations[::-1]):
                platforms.append((pt[0] + platform_template.shape[1] // 2, pt[1]))
        return platforms

    def _detect_ball(self, frame_gray):
        result = cv2.matchTemplate(frame_gray, self.ball_template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        locations = np.where(result >= threshold)

        balls = []
        for pt in zip(*locations[::-1]):
            balls.append((pt[0] + self.ball_template.shape[1] // 2, pt[1] + self.ball_template.shape[0]))
        return balls

    def process_frame(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        platforms = self._detect_platforms(frame_gray)
        balls = self._detect_ball(frame_gray)

        for platform in platforms:
            pt1 = (platform[0] - self.platform_templates[0].shape[1] // 2, platform[1])
            pt2 = (
                platform[0] + self.platform_templates[0].shape[1] // 2,
                platform[1] + self.platform_templates[0].shape[0],
            )
            cv2.rectangle(frame, pt1, pt2, (0, 255, 0), 1)

        for ball in balls:
            pt1 = (ball[0] - self.ball_template.shape[1] // 2, ball[1] - self.ball_template.shape[0])
            pt2 = (ball[0] + self.ball_template.shape[1] // 2, ball[1])
            cv2.rectangle(frame, pt1, pt2, (0, 0, 255), 1)

        return frame, platforms, balls
