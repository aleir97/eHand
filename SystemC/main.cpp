#define SC_INCLUDE_FX

#include "systemc.h"
#include "consumidor.h"
#include "productor.h"
#include "inference.h"
#include "fifo.h"

class top : public sc_module{
	public:
		fifo_T<sc_fixed<10,5>> *Qinputs, *Qweights, *Qbias, *Qoutputs;
		productor *instProductor;
		consumidor *instConsumidor;
		inference *instRNA; 
		
		
	//the module constructor
	SC_CTOR(top) {
		instProductor = new productor("DatosEntrada", "weigths.txt", "bias.txt", "inputs.txt");
		instConsumidor = new consumidor("SalidaResultados","resultados.txt");
		instRNA = new inference("RNA");
		

		Qinputs = new fifo_T<sc_fixed<10,5>>("Qinputs", 4); 
		Qweights = new fifo_T<sc_fixed<10,5>>("Qweights", 1);
		Qbias = new fifo_T<sc_fixed<10,5>>("Qbias", 1);  
		Qoutputs = new fifo_T<sc_fixed<10,5>>("Qoutputs", 1); 

		instProductor -> input_out( *Qinputs);
		instProductor -> weight_out( *Qweights);
		instProductor -> bias_out( *Qbias);
		
		instConsumidor -> output_in( *Qoutputs);

		instRNA -> input( *Qinputs);
		instRNA -> weight_in( *Qweights);
		instRNA -> bias_in( *Qbias);
		instRNA -> output( *Qoutputs);

	}

};


int sc_main(int nargs, char* vargs[]){
	top principal("top");
	sc_start();

	return 0;
}
