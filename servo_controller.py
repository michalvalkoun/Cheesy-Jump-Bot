import time

import serial


class ServoController:
    def __init__(self, port="COM5", baudrate=9600, min_angle=0, max_angle=180):
        self.ser = serial.Serial(port, baudrate)
        self.min_angle = min_angle
        self.max_angle = max_angle
        time.sleep(2)

    def set_servo_angle(self, angle):
        if self.min_angle <= angle <= self.max_angle:
            self.ser.write(f"{angle}\n".encode())
        else:
            print("Invalid angle. Angle must be between 0 and 180.")

    def close(self):
        self.ser.close()
