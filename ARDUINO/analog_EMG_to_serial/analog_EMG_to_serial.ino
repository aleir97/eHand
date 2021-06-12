#define EMG_PIN1 0
#define EMG_PIN2 1
#define samplerate 1000; // Hz

short unsigned int tpersample = 1000/samplerate; // Milliseconds

void setup() {   
    Serial.begin(115200);
    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    short unsigned int time = 0;

    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    delay(1000);
           
    if (Serial.available()){
      digitalWrite(LED_BUILTIN, HIGH);

      Serial.println("ini");
          
      while(true)    
        if (time <= millis()){
          time = millis();
          
          Serial.println(analogRead(EMG_PIN1));    
          Serial.println(analogRead(EMG_PIN2));
        
          time = time + tpersample;
        }
    }
}
