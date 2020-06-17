#ifndef CONSUMIDOR_H
#define CONSUMIDOR_H

#define SC_INCLUDE_FX

#include "systemc.h"
#include "fifo.h"
#include <stdio.h>

SC_MODULE (consumidor) {
	public:
		sc_port<read_if_T<sc_fixed<10,5>>> output_in; 

		SC_HAS_PROCESS(consumidor);

	void consumir(){
		sc_fixed<10,5> resRNA;
		double dato, rst;
		int i;


		for(i=0; i < 6; ++i){
			output_in ->read( resRNA ); 
			//fscanf(fichero, "%l", &dato);
			
			//Linea añadida para comprobar en el debugger lo que entra por audio_in
			
			printf("!!: %lf \n", resRNA.to_double());

			//if(dato != rst)
				//printf("Error @ %d : %d <> %d\n", i, dato,  resRNA.to_double());
			
		}

		//fclose(fichero);
		sc_stop();

	}

	consumidor(sc_module_name name_, char *fileName) : sc_module(name_){
		cout<<"consumidor: " << name() << "  " << fileName << endl;
    	
        fichero = fopen(fileName, "rt");
	    if(!fichero){
		    fprintf(stderr, "No es posible abrir el fichero %s\n", fileName);
		    exit(-1);
	    }
        
        SC_THREAD(consumir);
	
	}

private:
    FILE *fichero;

}; 

#endif
