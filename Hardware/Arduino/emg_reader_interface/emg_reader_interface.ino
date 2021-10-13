#include "EMGFilters.h"

#define TIMING_DEBUG 1
#define SensorInputPin1 A0 
#define SensorInputPin2 A1  

//Objeto de la libreria EMGFilters
EMGFilters myFilter;

//Rate de muestreo 
SAMPLE_FREQUENCY sampleRate = SAMPLE_FREQ_1000HZ;

//Frecuencia de ruido producida por la alimentacion (depende del pais)
NOTCH_FREQUENCY humFreq = NOTCH_FREQ_50HZ;

unsigned long timeStamp;
unsigned long timeBudget;


//Limites de calibración
int Threshold1 = 0, Threshold2 = 0;

bool calibration(){//Funcion para calibracion de las placas
    int max1= 0, max2= 0, i= 0, margin= 200;
    int Value1= 0, Value2= 0, DataAfterFilter1= 0, DataAfterFilter2= 0, envlope1= 0, envlope2= 0;

    for (i = 0; i < 2000; i++){
        //Leemos por los canales analogico/digital las muestras de las 2 placas
        Value1 = analogRead(SensorInputPin1);
        Value2 = analogRead(SensorInputPin2);
    
        //Filtramos las 2 entradas
        DataAfterFilter1 = myFilter.update(Value1);
        DataAfterFilter2 = myFilter.update(Value2);

        envlope1 = sq(DataAfterFilter1);
        envlope2 = sq(DataAfterFilter2);

        max1 = (envlope1 > max1) ? max1 : envlope1;
        max2 = (envlope2 > max2) ? max2 : envlope2;
    }  
    
    //Una vez tenemos los valores maximos medidos en reposo les sumamos un margen
    max1 += margin;
    max2 += margin;

    Threshold1 = max1;
    Threshold2 = max2;

    return false;
}

void setup() {   
    Serial.begin(115200);
    
    //Inicializamos el filtro
    myFilter.init(sampleRate, humFreq, true, true, true);
    
    //Calculo del tiempo para 2 muestras
    timeBudget = 2* (1e6 / sampleRate);

    //Led que nos indicará final de calibración
    pinMode(LED_BUILTIN, OUTPUT);
    //Calibracion de la mano
    while (calibration()){
    }      
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
    DataAfterFilter1 = myFilter.update(Value1);
    DataAfterFilter2 = myFilter.update(Value2);

    envlope1 = sq(DataAfterFilter1);
    envlope2 = sq(DataAfterFilter2);
    
    envlope1 = (envlope1 > Threshold1) ? envlope1 : 0;
    envlope2 = (envlope2 > Threshold2) ? envlope2 : 0;

    //Calculo del tiempo que necesitan los filtros
    timeStamp = micros() - timeStamp;
    if (TIMING_DEBUG) {
        // Serial.print("DATOS LEIDOS SIN FILTRAR "); Serial.println(Value1);Serial.println(Value2);
        
        // Serial.print("DATOS FILTRADOS "); Serial.println(DataAfterFilter1);Serial.println(DataAfterFilter2);
        
        Serial.print(" DTO PROCESADO EMG1 ");
        Serial.println(envlope1);
        Serial.print(" DTO PROCESADO EMG2 ");
        Serial.println(envlope2);
        
        // Serial.print("T DE FILTRADO "); Serial.println(timeStamp);
    }

    // if less than timeBudget, then you still have (timeBudget - timeStamp) to
    // do your work
    delayMicroseconds(500);
    // if more than timeBudget, the sample rate need to reduce to
    // SAMPLE_FREQ_500HZ
}
