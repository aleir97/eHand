#include "EMGFilters.h"

#define TIMING_DEBUG 1
#define SensorInputPin1 0 
#define SensorInputPin2 1  

//Objeto de la libreria EMGFilters
EMGFilters myFilter1;
EMGFilters myFilter2;

//Rate de muestreo 
//SAMPLE_FREQUENCY sampleRate = SAMPLE_FREQ_1000HZ;
SAMPLE_FREQUENCY sampleRate = SAMPLE_FREQ_500HZ;
//Frecuencia de ruido producida por la alimentacion (depende del pais)
NOTCH_FREQUENCY humFreq = NOTCH_FREQ_50HZ;

unsigned long timeStamp;
unsigned long timeBudget;

void setup() {   
    Serial.begin(115200);
    Serial.println("CH1:, CH2:");
    
    //Inicializamos el filtro
    myFilter1.init(sampleRate, humFreq, true, true, true);
    myFilter2.init(sampleRate, humFreq, true, true, true);
    
    //Calculo del tiempo para 2 muestras
    timeBudget = 2* (1e6 / sampleRate);
 
}

void loop() {
    int Value1= 0, Value2= 0, DataAfterFilter1= 0, DataAfterFilter2= 0, envlope1= 0, envlope2= 0;

    //Encedemos el led indicando que la calibracion fue terminada
    digitalWrite(LED_BUILTIN, HIGH);

    timeStamp = micros();

    //Leemos por los canales analogico/digital las muestras de las 2 placas
    Value1 = analogRead(SensorInputPin1);
    Value2 = analogRead(SensorInputPin2);
    
    //Filtramos las 2 entradas
    DataAfterFilter1 = myFilter1.update(Value1);
    DataAfterFilter2 = myFilter2.update(Value2);

    envlope1 = sq(DataAfterFilter1);
    envlope2 = sq(DataAfterFilter2);
   
    //envlope1 = (envlope1 > Threshold1) ? envlope1 : 0;
    //envlope2 = (envlope2 > Threshold2) ? envlope2 : 0;

    //Calculo del tiempo que necesitan los filtros
    timeStamp = micros() - timeStamp;
    if (TIMING_DEBUG) {
        // Serial.print("DATOS LEIDOS SIN FILTRAR "); 
        //Serial.print(Value1);
        //Serial.print(" ");
        //Serial.println(Value2);
        
        //Serial.print("DATOS FILTRADOS "); 
        //Serial.print(DataAfterFilter1);
        //Serial.print(" ");
        //Serial.println(DataAfterFilter2);
      
        Serial.print(envlope1);
        Serial.print(" ");
        Serial.println(envlope2);

        //Serial.print("T DE FILTRADO "); Serial.println(timeStamp);
    }

    // if less than timeBudget, then you still have (timeBudget - timeStamp) to
    // do your work
    //delayMicroseconds(500);
    // if more than timeBudget, the sample rate need to reduce to
    // SAMPLE_FREQ_500HZ
}
