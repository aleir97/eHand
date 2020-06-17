#ifndef FIFO_H
#define FIFO_H

#include"systemc.h"
#include<stdio.h>

template <class T>
class write_if_T : virtual public sc_interface
{
public:
	virtual void write(T) = 0;
	virtual void reset() = 0;
};

template <class T>
class read_if_T : virtual public sc_interface
{
public:
	virtual void read(T &) = 0;
	virtual int num_available() = 0;
};

template <class T>
class fifo_T : public sc_channel,
	public write_if_T<T>,
	public read_if_T<T>
{
public:

SC_HAS_PROCESS(fifo_T);

fifo_T( sc_module_name name_, int max_=5000) :  sc_module(name_)
{
	max = max_;
	data = new T[max];
	num_elements = first = 0;
	inspecciona = false;
}

~fifo_T(){ delete data;}
void setInspect()	{ inspecciona = true;  }
void resetInspect()	{ inspecciona = false; }

void write(T c) {
if (num_elements == max)
	wait(read_event);
	data[(first + num_elements) % max ] = c;
	if(inspecciona) cout << name() << hex << " " << c << endl;
	++ num_elements;
	write_event.notify();
}
void read(T& c) {
	if (num_elements == 0)
	wait(write_event);
	c = data[first];
	-- num_elements;
	first = (first + 1) % max;
	read_event.notify();
} 
void reset() { num_elements = first = 0; }
int num_available() {return num_elements;}


private:
	int max; 
	T *data;
	int num_elements, first;
	sc_event write_event, read_event;
	bool inspecciona;
};




template <class T>
class endlessQueue_T : public sc_channel,
	public write_if_T<T>,
	public read_if_T<T>
{
public:

SC_HAS_PROCESS(endlessQueue_T);

endlessQueue_T( sc_module_name name_) :  sc_module(name_)
{
	num_elements = 0;
	inspecciona = false;
}

void setInspect()	{ inspecciona = true;  }
void resetInspect()	{ inspecciona = false; }

void write(T c) {
	data = c;
	num_elements = 1;
	if(inspecciona) cout << name() << hex << " " << c << endl;
	write_event.notify();
}
void read(T& c) {
	if (num_elements == 0)
	wait(write_event);
	c = data;
	read_event.notify();
} 
void reset() { num_elements = 0; }
int num_available() {return num_elements;}


private:
	T data;
	int num_elements;
	sc_event write_event, read_event;
	bool inspecciona;
};




template <class T>
class constSrc_T : public sc_channel,
	public read_if_T<T>
{
public:

SC_HAS_PROCESS(constSrc_T);

constSrc_T( sc_module_name name_, T constante_) :  sc_module(name_)
{
	constante = constante_; 
}

void read(T& c) {
	c = constante;
	read_event.notify();
} 	
int num_available() {return 1;}

private:
	T constante;
	sc_event read_event;
};


template <class T>
class ManyConstSrc_T : public sc_channel,
	public read_if_T<T>
{
public:

SC_HAS_PROCESS(ManyConstSrc_T);

ManyConstSrc_T( sc_module_name name_, T *constantes_, int num_) :  sc_module(name_)
{
	constantes = new T[num_];
	for(int i; i<num_; ++i)	constantes[i] = constantes_[i];
	num = num_;		turno = 0;
}

~ManyConstSrc_T(){	delete constantes; }

void read(T& c) {
	c = constantes[turno++];
	if(turno == num)	turno = 0;
	read_event.notify();
} 	
int num_available() {return 1;}

private:
	T *constantes;
	int num, turno;
	sc_event read_event;
};


template <class T>
class sumidero_T : public sc_module{
public:
	sc_port<read_if_T< T >>  inp;

SC_HAS_PROCESS(sumidero_T);

sumidero_T( sc_module_name name_) :  sc_module(name_)
{
	SC_THREAD( read ); 
}

void read() {
	T dummy; 
	while(true)
		inp->read( dummy ); 
}
};




#endif