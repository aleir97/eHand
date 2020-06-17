#ifndef PRODUCTOR_H
#define PRODUCTOR_H

#define SC_INCLUDE_FX

#include "systemc.h"
#include "fifo.h"
#include <stdio.h>
#include <math.h>

SC_MODULE (productor) {
	public:
		sc_port<write_if_T<sc_fixed<10,5>>> input_out, weight_out, bias_out;	

		SC_HAS_PROCESS(productor);

	void producir(){
		sc_fixed<10,5> bias, weight, input;
		double weightDT, biasDT, inputDT ;
		

		//Escaneamos los bias 3
		while (fscanf(biasFL, "%lf", &biasDT) != EOF){
			bias =  biasDT;
			bias_out -> write(bias);
			
		}
		fclose(biasFL);
		
		//Escaneamos los pesos 3
		while (fscanf(weightFL, "%lf", &weightDT) != EOF){
			weight =  weightDT;
			weight_out -> write(weight);
			
		}
		fclose(weightFL);

		//Escaneamos input 
		while (fscanf(inputFL, "%lf", &inputDT) != EOF){
			input =  inputDT;
			input_out -> write(input);
			
		}
		fclose(inputFL);
		wait();
	}


	productor(sc_module_name name_, char *fileName1, char *fileName2, char *fileName3) : sc_module(name_){
		cout<<"productor: " << name() << "  " << endl;
    	
		weightFL = fopen(fileName1, "rt");
	    if(!weightFL){
		    fprintf(stderr, "No es posible abrir el fichero %s\n", fileName1);
		    exit(-1);
	    }

		biasFL = fopen(fileName2, "rt");
	    if(!biasFL){
		    fprintf(stderr, "No es posible abrir el fichero %s\n", fileName2);
		    exit(-1);
	    }

		inputFL = fopen(fileName3, "rt");
	    if(!inputFL){
		    fprintf(stderr, "No es posible abrir el fichero %s\n", fileName3);
		    exit(-1);
	    }

		SC_THREAD(producir);

	}
private:
	FILE *weightFL, *biasFL, *inputFL;

}; 

#endif