#include "inference.h"

void inference::do_inference(){
    sc_int<2> i= 1, o= 1; //Numero de neuronas en capa de entrada(i) y salida(o)
    sc_int<4> f= 1, s= 1; //Numero de neuronas en capas intermedias
    sc_fixed<10,5> bias, weights, inputs, outputs; //Variables para lectura de bias y pesos

    //Variables temporales
    sc_int<2> m;  
    sc_int<4> n, j;


    double M_input[i.to_int()], M_output[o.to_int()], M_hidden_1[f.to_int()],  M_hidden_2[s.to_int()];
	double M_weight_1[f.to_int()][i.to_int()], M_weight_2[s.to_int()][f.to_int()], M_weight_3[o.to_int()][s.to_int()];
	double M_bias_1[f.to_int()], M_bias_2[s.to_int()], M_bias_3[o.to_int()];
    double M_temp_1[i.to_int()][f.to_int()], M_temp_2[f.to_int()][s.to_int()], M_temp_3[s.to_int()][o.to_int()];


    int correct_value, stored_values= 0, c1= 0, c2= 0;
    int i_f= i.to_int()*f.to_int(), f_s= f.to_int()*s.to_int(), s_o= s.to_int()*o.to_int();


    //Almacenamos los valores de los bias
    for (stored_values= 0; stored_values < f.to_int() + s.to_int() + o.to_int(); stored_values++){
        bias_in -> read(bias);
        double check = bias;

        if (stored_values < f)    
            M_bias_1[stored_values] = bias.to_double();

        else if (stored_values >= f && stored_values < (f+s))
            M_bias_2[stored_values - f] = bias.to_double(); 

        else if (stored_values >= (f+s))
            M_bias_3[stored_values -f -s] = bias.to_double();
        
    }

    //Almacenamos los valores de los pesos
    for (stored_values= 0; stored_values < i_f + f_s + s_o; stored_values++){
        weight_in -> read(weights);
        double check = weights;

        if (stored_values < i_f){
            c1 = stored_values / i.to_int();
            c2 = stored_values % i.to_int();

            M_weight_1[c1][c2]= weights.to_double();
        }

        if(stored_values >= i_f && stored_values < (i_f + f_s)){
            c1 = (stored_values - i_f) / f.to_int();
            c2 = (stored_values - i_f) % f.to_int();

            M_weight_2[c1][c2] = weights.to_double();
        }

        if(stored_values >= (i_f + f_s) && stored_values < (i_f + f_s + s_o)){
            c1 = (stored_values - (i_f + f_s)) / s.to_int();
            c2 = (stored_values - (i_f + f_s)) % s.to_int();

            M_weight_3[c1][c2]= weights.to_double();
        }
    }

    while (true){

        //Cargamos los valores en la capa de entrada
        for(stored_values= 0; stored_values < i; stored_values++){
            input -> read(inputs);
            double check = inputs;
            M_input[stored_values]= inputs.to_double();
        }

        //Los valores de la primera capa son la suma de productos de la matriz de la entrada y los pesos almacenados 
        for(m= 0; m < i; m++)
            for(n= 0; n < f; n++)
                M_temp_1[m][n] = M_input[m] * M_weight_1[n][m];
        
        for (n= 0; n < f; n++)
		    for (m= 0; m < i; m++)
			    M_hidden_1[n] += M_temp_1[m][n];

	    for (n= 0; n < f; n++)
			M_hidden_1[n] += M_bias_1[n];

        for (n= 0; n < f; n++)
		    M_hidden_1[n] = 1.0/(1.0 + exp((-M_hidden_1[n]))); //sigmoid function approximation
        

        //Los valores de la segunda capa son la suma de productos de la matriz de la primera capa y los pesos almacenados 
        for (n= 0; n < f; n++)
            for (j= 0; j < s; j++)
                M_temp_2[n][j] = M_hidden_1[n] * M_weight_2[j][n];


        for (j= 0; j < s; j++)
            for (n= 0; n < f; n++)
                M_hidden_2[j] += M_temp_2[n][j];


        for (j= 0; j < s; j++)
            M_hidden_2[j] += M_bias_2[j];


        for (j= 0; j < s; j++)
            M_hidden_2[j] = 1.0/(1.0 + exp((-M_hidden_2[j])));
    
        
        //Los valores de la capa de salida son la suma de productos de la matriz de la segunda capa y los pesos almacenados 
	    for (j= 0; j < s; j++)
			for (m= 0; m < o; m++)
				M_temp_3[j][m] = M_hidden_2[j] * M_weight_3[m][j];

        
        //Calculo de salida
	    for (m= 0; m < o; m++)
		    for(j= 0; j < s; j++)
			    M_output[m] += M_temp_3[j][m];

	    for (m= 0; m < o; m++)
		    M_output[m] += M_bias_3[m];

	    for (m= 0; m < o; m++){
		    M_output[m] = 1.0/(1.0 + exp((-M_output[m])));

            outputs =  M_output[m]; 
            output -> write(outputs);
        }
    }
}

