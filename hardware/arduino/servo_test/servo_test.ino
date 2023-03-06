#include <Servo.h>
Servo servo1, servo2;

void setup() {
    servo1.attach(8);
    servo2.attach(9);

	static int angle = 180;
	static int angle2 = 0;
	servo1.write(angle);
	servo2.write(angle2);
}

void loop() {

}
