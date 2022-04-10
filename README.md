# Ferromagnetic-surface-simulation
The goal of this topic is to model ferromagnetic materials features using ```PyGame``` engine and ```Matplotlib```.
## The studied phenomenon
Indeed, a ferromagnetic surface has for main characteristic a spontaneous magnetization presence which appears after a magnetic field is applied on it. However this magnet effect may vanish if the temperature where this material is increase. This is what we call Curie's temperature.

To represent properly this effect, we need to define the total magnetization **S**. It is the magnetization sum of every element **dS**. In fact every **dS** element corresponds to a mass of electrons. Each electron posses it's own spin which is either positive or negativ which means that every element **dS** is globaly positiv or negativ. To simplify that we will admit that **dS** is either equal to 1 or -1. This means that for **n** elements **dS** we have the following properties:

<p align="center">
<img src="https://latex.codecogs.com/png.image?\dpi{110}{\color{White}&space;S&space;=&space;\sum_{1}^{n}&space;dS&space;=&space;0&space;\Leftrightarrow&space;magnetization&space;=&space;0}">
</p>
<p align="center"> 
<img src="https://latex.codecogs.com/png.image?\dpi{110}{\color{White}&space;S&space;=&space;\sum_{1}^{n}&space;dS&space;=&space;n&space;\Leftrightarrow&space;magnetization&space;=&space;full}">
</p>

Moreover, two parameters affect the system such as:
* Each elements **dS** work like a small magnet side by side, the tendancy of these magnets is to have the same spin as their neighboors to minimise the global energy. This characteristic minimise the entropy.
* As the temperature is rising, it creates a termic hustle. Because of that, it increases the probability that a random element **dS** may change it's global spin. This characteristic increases the entropy.

## The model
Our program need to observ the development of a ferromagnetic surface. To model that, we will plot in real time global energy fluctuation as well as an **NxN** grid which modelises differents magnetic areas. The grid as well as the global energy fluctuation is responsive to the temperature fluctuation. The temperature is directly controlled by the user using a slider.

## Preview of the final result
Here is a preview of what we want to model:

<p align="center">
  
![finalResult](https://user-images.githubusercontent.com/72025267/162620772-4e1a14d2-b261-4dcf-9553-4e64ef5d829d.gif)
  
</p>

## Solving of the problem

