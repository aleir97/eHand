/*
    - Script to acquire and process EMG samples from the Olimex © 1997-2022 SHIELD-EKG-EMG board
    
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

#include "EMGFilters.h"

#define EMG_CH1 0 
#define EMG_CH2 1    

#define samplerateHz 1000; // Hz
#define SYNC_FLAG 0xaa

short unsigned int time = 0;
short unsigned int tpersample = 1000/samplerateHz; // Milliseconds

//Objeto de la libreria EMGFilters
EMGFilters myFilter1;
EMGFilters myFilter2;

//Rate de muestreo 
SAMPLE_FREQUENCY sampleRate = SAMPLE_FREQ_1000HZ;

//Frecuencia de ruido producida por la alimentacion (depende del pais)
NOTCH_FREQUENCY humFreq = NOTCH_FREQ_60HZ;

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
	Serial.begin(115200);
    
	//Inicializamos el filtro
	myFilter1.init(sampleRate, humFreq, true, false, true);
	myFilter2.init(sampleRate, humFreq, true, false, true);

	pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
	int value1 = 0, DataFiltered1= 0;
	int value2 = 0, DataFiltered2= 0;
  
	digitalWrite(LED_BUILTIN, HIGH);

	if(is_arduino_sync()){
		digitalWrite(LED_BUILTIN, LOW);
 	  	while(Serial.read() == -1){    
	  		if (time <= millis()){
          		time = millis();
          
				value1 = analogRead(EMG_CH1);
          		DataFiltered1 = myFilter1.update(value1);

          		value2 = analogRead(EMG_CH2);
          		DataFiltered2 = myFilter2.update(value2);
          
          		Serial.println(DataFiltered1);         
          		Serial.println(DataFiltered2);
            
          		time = time + tpersample;
        	}
       	}
  	}  
}