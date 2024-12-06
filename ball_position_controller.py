import cv2


class BallPositionController:
    def __init__(self, center_angle, angle_margin):
        self.center_angle = center_angle
        self.angle_margin = angle_margin

    def adjust_servo_position(self, platforms, balls, servo_controller, frame):
        if not platforms or not balls:
            servo_controller.set_servo_angle(self.center_angle)
            return

        lowest_platform = max(platforms, key=lambda p: p[1])
        ball_center_x = balls[0][0]
        platform_center_x = lowest_platform[0]
        margin = 50

        if ball_center_x < platform_center_x - margin:
            servo_controller.set_servo_angle(self.center_angle + self.angle_margin)
        elif ball_center_x > platform_center_x + margin:
            servo_controller.set_servo_angle(self.center_angle - self.angle_margin)
        else:
            servo_controller.set_servo_angle(self.center_angle)

        self.draw_target_rectangle(frame, lowest_platform)

    def draw_target_rectangle(self, frame, platform):
        top_left = (platform[0] - 50, platform[1] - 10)
        bottom_right = (platform[0] + 50, platform[1] + 10)
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 255), 1)
