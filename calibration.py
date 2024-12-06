"""
Servo Motor Calibration Tool for cheesy jump bot

This module provides functionality to control and calibrate a servo motor
using Pygame and serial communication.

Author: Michal Valkoun
Version: 1.0.0
Date: 2024-12-04
License: MIT License
"""

import time

import pygame

from servo_controller import ServoController

MIN_ANGLE = 0
MAX_ANGLE = 180


class Calibration:
    def __init__(self, start_angle=90, margin=30, mode="control"):
        pygame.init()
        self.servo_controller = ServoController(min_angle=MIN_ANGLE, max_angle=MAX_ANGLE)
        self.start_angle = start_angle
        self.margin = margin
        self.mode = mode
        self.current_angle = self.start_angle
        self.servo_controller.set_servo_angle(self.current_angle)
        self.font = pygame.font.SysFont("Arial", 20)
        self.screen = pygame.display.set_mode((450, 270))
        pygame.display.set_caption("Servo Control")

    def process_key_inputs(self):
        keys = pygame.key.get_pressed()
        if self.mode == "control":
            self.adjust_angle_control_mode(keys)
        elif self.mode == "calibration":
            self.adjust_angle_calibration_mode(keys)
        self.adjust_margin(keys)
        self.servo_controller.set_servo_angle(self.current_angle)

    def adjust_angle_control_mode(self, keys):
        if keys[pygame.K_a]:
            self.current_angle = max(MIN_ANGLE, self.start_angle - self.margin)
        elif keys[pygame.K_d]:
            self.current_angle = min(MAX_ANGLE, self.start_angle + self.margin)
        else:
            self.current_angle = self.start_angle

    def adjust_angle_calibration_mode(self, keys):
        if keys[pygame.K_a]:
            self.current_angle = max(MIN_ANGLE, self.current_angle - 1)
        elif keys[pygame.K_d]:
            self.current_angle = min(MAX_ANGLE, self.current_angle + 1)
        self.start_angle = self.current_angle

    def adjust_margin(self, keys):
        if keys[pygame.K_w]:
            self.margin = min(MAX_ANGLE, self.margin + 1)
        elif keys[pygame.K_s]:
            self.margin = max(1, self.margin - 1)

    def update_display(self):
        self.screen.fill((0, 0, 0))
        self.render_text(f"Mode: {self.mode.capitalize()}", 20, 20)
        self.render_text(f"Current Angle: {self.current_angle}", 20, 50)
        self.render_text(f"Margin: {self.margin}", 20, 80)
        self.render_text("Controls:", 20, 120)
        self.render_text("  - 'M' to toggle mode", 20, 145)
        self.render_text("  - 'A' / 'D' to adjust angle", 20, 170)
        self.render_text("  - 'W' / 'S' to adjust margin", 20, 195)
        pygame.display.update()

    def render_text(self, text, x, y):
        self.screen.blit(self.font.render(text, True, (255, 255, 255)), (x, y))

    def run(self):
        try:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_program()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                        self.mode = "calibration" if self.mode == "control" else "control"
                self.process_key_inputs()
                self.update_display()
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.quit_program()

    def quit_program(self):
        pygame.quit()
        self.servo_controller.close()
        exit()


def main():
    Calibration(mode="calibration", start_angle=109, margin=40).run()


if __name__ == "__main__":
    main()
