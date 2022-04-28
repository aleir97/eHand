#include <string.h>

// If you wanna graph both signals in real time.    
#define DEBUG 1
#define EMG_CH1 34
#define EMG_CH2 33
#define samplerate 1000; // Hz

short unsigned int time_ = 0;
short unsigned int tpersample = 1000/samplerate; // Milliseconds

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(500);
  //analogReadResolution(9);
  analogSetWidth(12);
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
        if (time_ <= millis()){
          time_ = millis();

          if (DEBUG){
            Serial.print(analogRead(EMG_CH1));
            Serial.print(" ");
            Serial.println(analogRead(EMG_CH2));
          
          }else{
            // We are using println for the python communication.
            Serial.println(analogRead(EMG_CH1));
            Serial.println(analogRead(EMG_CH2));
          } 
          
          time_ = time_ + tpersample;
        }
      }
      Serial.read();
    }
  }
}
