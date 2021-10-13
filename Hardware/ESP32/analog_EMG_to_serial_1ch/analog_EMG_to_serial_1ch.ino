#include <string.h>

#define EMG_CH1 34
#define samplerate 1000; // Hz

// This code is a DEMO for playing with 1 channel

short unsigned int time_ = 0;
short unsigned int tpersample = 1000/samplerate; // Milliseconds

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(500);
 
  pinMode(LED_BUILTIN, OUTPUT);
}

int sensorValue = 0;
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
        if (time_ <= millis()){
          time_ = millis();
   
          // We are using println for the python communication.
          sensorValue = analogRead(EMG_CH1);
    
          Serial.println(sensorValue);
           
          time_ = time_+ tpersample;
        }
      }
      Serial.read();
    }
  }
}
