#ifndef INFERENCE_H
#define INFERENCE_H

#define SC_INCLUDE_FX

#include "systemc.h"
#include "fifo.h"

SC_MODULE(inference) {
    public:
        sc_port<read_if_T<sc_fixed<10,5>>> input, weight_in, bias_in;
        sc_port<write_if_T<sc_fixed<10,5>>> output;
      
        void do_inference();
    
        SC_HAS_PROCESS(inference);

        inference(sc_module_name name_) : sc_module(name_){
            cout<<"inference: "<<name()<<endl;

            SC_THREAD(do_inference);  
        }
}; 

#endif
