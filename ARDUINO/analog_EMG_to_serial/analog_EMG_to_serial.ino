#define EMG_CH1 0
#define EMG_CH2 1
#define samplerate 1000; // Hz

short unsigned int time = 0;
short unsigned int tpersample = 1000/samplerate; // Milliseconds

void setup() {   
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {  
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
      
  if (Serial.readString() == "ini"){
    digitalWrite(LED_BUILTIN, HIGH);

    Serial.read();
    Serial.println("ini");    

    // If you wanna graph both signals in real time.    
    //Serial.println("CH1:, CH2:");
            
    while(!Serial.available()){    
      Serial.read();
      if (time <= millis()){
        time = millis();

        // If you wanna graph both signals in real time.    
        /*Serial.print(analogRead(EMG_CH1));
        Serial.print(" ");
        Serial.println(analogRead(EMG_CH2));
        */
        
        // We are using printl for the python communication.
        Serial.println(analogRead(EMG_CH1));
        Serial.println(analogRead(EMG_CH2));
         
        time = time + tpersample;
      }
    }
    Serial.read();
  }
}
