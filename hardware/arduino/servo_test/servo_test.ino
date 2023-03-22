#include <Servo.h>
Servo servo1, servo2;

void setup() {
    servo1.attach(9);
	pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
	static int angle = 180;
	static int angle2 = 0;
	static int angle3 = 94;
	static int angle4 = 150;
	static int angle5 = 130;

	servo1.write(angle3);
	digitalWrite(LED_BUILTIN, HIGH);
	delay(10000);
	digitalWrite(LED_BUILTIN, LOW);

	servo1.write(angle);
	delay(3000);
	servo1.write(angle4);
	delay(2000);
	servo1.write(angle5);
	delay(3000);

	servo1.write(angle2);
	delay(1500);
}
