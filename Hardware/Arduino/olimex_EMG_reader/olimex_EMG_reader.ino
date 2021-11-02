#include "EMGFilters.h"

// If you wanna graph both signals in real time.    
#define EMG_CH1 0   

#define samplerate 1000; // Hz

short unsigned int time = 0;
short unsigned int tpersample = 1000/samplerate; // Milliseconds

//Objeto de la libreria EMGFilters
EMGFilters myFilter1;

//Rate de muestreo 
SAMPLE_FREQUENCY sampleRate = SAMPLE_FREQ_1000HZ;

//Frecuencia de ruido producida por la alimentacion (depende del pais)
NOTCH_FREQUENCY humFreq = NOTCH_FREQ_50HZ;

unsigned long timeStamp;

void setup() {   
  Serial.begin(115200);
    
  //Inicializamos el filtro
  myFilter1.init(sampleRate, humFreq, true, true, true);

  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  int value1 = 0, envlope1= 0, DataFiltered1= 0;
  
  digitalWrite(LED_BUILTIN, HIGH);
  delay(500);
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  
  if (Serial.available()){
    if (Serial.readString() == "ini"){
      digitalWrite(LED_BUILTIN, HIGH);
  
      // Python Sync  
      Serial.println("ini");
      //Serial.read();    
    
      while(!Serial.available()){    
        Serial.read();
        if (time <= millis()){
          time = millis();
          
          value1 = analogRead(EMG_CH1);
          DataFiltered1 = myFilter1.update(value1);
          DataFiltered1 = abs(DataFiltered1);
          //DataFiltered1 = DataFiltered1 * DataFiltered1 ;
          
          Serial.println(DataFiltered1);         
          Serial.println("0");      
            
          time = time + tpersample;
        }
      }
      Serial.read();
    }
  }  
}
