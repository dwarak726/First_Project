#include <Servo.h>  // Include Servo library

Servo myServo;      // Create servo object

void setup() {
  myServo.attach(9);       // Attach servo to pin 9
  Serial.begin(115200);    // Start serial communication
  myServo.write(0);        // Set servo to initial position
}

void loop() {
  if (Serial.available() > 0) {     // Check for incoming data
    char command = Serial.read();   // Read one character from serial

    if (command == '1') {
      myServo.write(90);            // Rotate to 90°
      delay(1000);                  // Wait for 5 seconds
      myServo.write(0);             // Return to initial position
    }
  }
}
