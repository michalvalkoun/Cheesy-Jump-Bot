#include <Servo.h>

Servo myServo;  // Create a servo object
int currentAngle = 90;  // Start at 90° (center) position

void setup() {
  myServo.attach(9);  // Attach the servo to pin 9
  Serial.begin(9600); // Start serial communication
  myServo.write(currentAngle);  // Move servo to center position at start
}

void loop() {
  if (Serial.available() > 0) {
    String angleString = Serial.readStringUntil('\n');  // Read string until newline
    int angle = angleString.toInt();  // Convert the string to an integer
    if (angle >= 0 && angle <= 180) {
      myServo.write(angle);  // Move servo to the specified angle
      currentAngle = angle;  // Update current angle
      delay(20);  // Small delay for servo to reach position
    }
  }
  // The servo stays in the last position until a new command is received
}
