[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://www.linkedin.com/in/aireguivalcarcel/)
[![GitHub contributors](https://img.shields.io/badge/-contributors-blue)](https://github.com/aleir97/ehand/graphs/contributors/)

<html>
  <head>
    <img src="https://1000marcas.net/wp-content/uploads/2019/12/UDC-emblema.jpg" high="300" width="500" class="center">
  </head>
</html>


# eHand
eHand is a technological, social, and totally Open Source project. It was born with the main motivation of building hardware and software applied to the EMG analysis done at the control of an electromechanical prosthesis.
During muscle activity, the few millivolts generated that conform the EMG are measured by electrodes and sensors. These same signals will then be converted from Analog to Digital by an Arduino that transmits the information to the PC via serial port, where a Python program is listening and in charge of the general system activity.
Finally, using mathematical tools for signal processing, eHand will extract classification patterns on the different desired movements to control any man-machine interface. Currently supports some web games and 3d models.

eHand se trata de un proyecto tecnológico, social y totalmente Open Source. Nació con la principal motivación de construir hardware y software aplicado al análisis EMG que se hace durante el control de una prótesis electro-mecánica.
Mediante sensores y electrodos se medirán los pocos milivoltios que se generan durante la actividad muscular y que conforman el EMG. Estas mismas señales, serán luego convertidas de Análogico a Digital por un Arduino y la información que se genere será enviada al PC via puerto serie, en donde habrá un programa de Python escuchando, encargado de la lectura y procesamiento general del sistema.\
Finalmente, mediante herramientas matemáticas para el procesado de señales, en este programa se extraerán patrones de clasificación sobre los diferentes movimientos deseados para con ellos controlar cualquier interfaz hombre-maquina. Actualmente soporta algunos juegos web y modelos 3d. 


<html>
  <head>
    <img src="https://github.com/aleir97/eHand/blob/master/documentation/misce/prostheses_general_architecture.png" high="300" width="500" class="center">
	<figcaption> Electromiography: Physiology, Engineering and Applications. </figcaption>
  </head>
</html>

Directory Structure
------
    .
    ├── documentation    # Related information about the project, images and technical PDF's
    ├── emg_data         # Database with EMG measurements used at analysis and processing
    ├── hardware         # Hardware main modules for signal acquisition at different hw combinations
        ├── arduino      # Arduino board core code
    └── python           # System modules, high-level signal processing, UX and UI
        ├── 3D           # Blender scripts and 3d models 
        ├── analysis     # Modules with digitial signal processing tools 
        ├── measuring    # Interface class for hardware communication, EMG measure reading and formating
        ├── models      	# Machine Learning modules used at pattern classification 
        └── utils        # Utils module
    └── eHand.py         # eHand main program


How to build and use
------
eHand needs some dedicated hardware like EMG sensors, electrodes and A/D conversor boards to run properly. Until now the software has been tested at Aliexpress and Olimex EMG sensors connected to an Arduino, nonetheless in the documentation
alternatives are presented. Feel free to use and test eHand at different platforms.
 
**Olimex SHIELD-EKG-EMG:**
<html>
  <head>
    <img src="https://www.olimex.com/Products/Duino/Shields/SHIELD-EKG-EMG/images/thumbs/310x230/SHIELD-EKG-EMG-01.jpg" high="150" width="400" onclick="">
  </head>
</html>

**Aliexpress Sensor de señal muscular, Sensor EMG para Arduino:**
<html>
  <head>
    <img src="https://ae01.alicdn.com/kf/HTB1CWTKayzxK1RkSnaVq6xn9VXaA.jpg" high="150" width="400" onclick="">
  </head>
</html>

If this hardware requirements are fullfilled, you can load and test their core software found at the hardware directory. Moreover, some python dependencies need and can be installed with:

```console
pip -install requirements.txt 
```

Now you can finally run the python main program eHand.py

### About me
    If you are interested in collaborating or just curious about it, contact me!
    Si estás interesado en colaborar con el proyecto o simplemente tienes curiosidad, contáctame!
    EMAIL: a.ireguiv@udc.es
    

