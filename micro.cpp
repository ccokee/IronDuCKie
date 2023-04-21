#include "Keyboard.h"

void setup() {
  // Start the serial communication at 9600 baud rate
  Serial.begin(9600);
  
  // Wait for the serial communication to be ready
  while (!Serial) {
    delay(10);
  }
  
  // Initialize the USB HID keyboard
  Keyboard.begin();
}

void loop() {
  // Check if there is data available on the serial port
  if (Serial.available() > 0) {
    // Read the keycode from the serial port
    char keycode = Serial.read();

    // Send the keycode as a USB HID keyboard key press
    Keyboard.press(keycode);
    delay(50);
    Keyboard.release(keycode);
  }
}
