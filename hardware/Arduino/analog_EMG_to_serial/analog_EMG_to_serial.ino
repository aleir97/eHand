#include <string.h>

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
#define DEBUG 1

#define EMG_CH1 0
#define EMG_CH2 1
#define samplerate 1000; // Hz

short unsigned int time = 0;
short unsigned int tpersample = 1000/samplerate; // Milliseconds

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(500);

  if (DEBUG)
    Serial.println("CH1:, CH2:");
   
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  
  if (Serial.available()){
    if (Serial.readString() == "ini"){
      digitalWrite(LED_BUILTIN, HIGH);
  
      // Python Sync
      Serial.read();
      Serial.println("ini");    
    
      while(!Serial.available()){    
        Serial.read();
        if (time <= millis()){
          time = millis();

          if (DEBUG){
            Serial.print(analogRead(EMG_CH1));
            Serial.print(" ");
            Serial.println(analogRead(EMG_CH2));
          
          }else{
            // We are using println for the python communication.
            Serial.println(analogRead(EMG_CH1));
            Serial.println(analogRead(EMG_CH2));
          } 
          
          time = time + tpersample;
        }
      }
      Serial.read();
    }
  }
}
