/*
    - Simple script to send samples from an analog port via Serial to a PC
    
	Copyright (C) 2021 Alejandro Iregui Valcarcel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

// If you wanna graph both signals in real time.    
// #define DEBUG 1

#define EMG_CH1 0
#define EMG_CH2 1
#define SAMPLERATE 1000; // Hz
#define SYNC_FLAG 0xaa

unsigned long time = 0;
short unsigned int tpersample = 1000/SAMPLERATE // Milliseconds

// AUX Functions
int is_arduino_sync(){
	if (Serial.read() == SYNC_FLAG){
   		digitalWrite(LED_BUILTIN, HIGH);
  		// Python Sync
   		Serial.write(SYNC_FLAG);    
		return 1;
	}
	return 0;	
}

void setup() {
	Serial.begin(115200); // Maximum Arduino serial speed
	Serial.setTimeout(500);

#ifdef DEBUG
	Serial.println("CH1:, CH2:");
	pinMode(LED_BUILTIN, OUTPUT);
#endif
}

void loop() {
	digitalWrite(LED_BUILTIN, HIGH);
	delay(1000);
	digitalWrite(LED_BUILTIN, LOW);
	delay(1000);
  
	if(is_arduino_sync()){
 	  	while(Serial.read() == -1){    
	  		if (time <= millis()){
        		time = millis();

				#ifdef DEBUG
				Serial.print(analogRead(EMG_CH1));
				Serial.print(" ");
				Serial.println(analogRead(EMG_CH2));

				#else
				// We are using println for the python communication.
				Serial.println(analogRead(EMG_CH1));
				Serial.println(analogRead(EMG_CH2));
				#endif

         		time = time + tpersample;
       		}
		}
	}
}
