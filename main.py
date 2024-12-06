import cv2
import pyautogui

from ball_and_platform_detector import BallAndPlatformDetector
from ball_position_controller import BallPositionController
from screen_capture import ScreenCapture
from servo_controller import ServoController


def main():
    servo_controller = ServoController()
    screen_capture = ScreenCapture()
    detector = BallAndPlatformDetector()
    position_controller = BallPositionController(center_angle=109, angle_margin=40)

    show_window = True

    while True:
        frame = screen_capture.capture()

        if frame is None:
            continue

        frame, platforms, balls = detector.process_frame(frame)
        position_controller.adjust_servo_position(platforms, balls, servo_controller, frame)

        if show_window:
            cv2.imshow("Platform and Ball Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()
    servo_controller.close()


if __name__ == "__main__":
    main()
