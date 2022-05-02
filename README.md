# Epidemic models using SNAP in python

In this project, I am using the Stanford network analysis project library in Python to apply my knowledge of SIR, SIS, and SIRS models into facebook network dataset. The aim of this project is to demonstrate how setting different parameters in the network model changes the spreading of behavior in the network.



## Running the code
Before deploying this project, please make sure you have installed python 3.7 in your device.

To deploy this project please first install SNAP through the following command:

```bash
  python -m pip snap-stanford
```

After that run the following to see the results of the models

```bash
  python file-name
```
## About the Epidemic Models
### SIR Model
The SIR model stands for the three states in epidemic model "Suceptible", "Infectious" and "Removed".
All nodes should start from the susceptible state first.
A behavior could start from any node (or even a group of nodes), and for each infectious node, there is a contagion probability *p* such that it passes the behavior to the neighbor susceptible node.
After a certain infectious time period, an infectious node could turn its state from infectious to removed, so that it cannot be infected anymore.

In the project file named SIRModel.py, there are 3 lists called susceptible, infectious and removed, which contains the list of nodes that has the corresponding state.
Users can try change the contagionProbability, infectiousTimePeriod and timeStep to see the effects it has to the network.

### SIS Model
The SIS model is very similar to the SIR model but this time instead of having the removed state, we turn infectious state back to suceptible state after the infectious time period. Hence we would expect that the spread to go on way more easier and broader given the same parameters.

### SIRS Model
The SIRS model is again a modification to the previous models. This time after the removed state, the nodes will return to the susceptible state, where the spread could go on again. So the spread will be expected to stay longer than SIS model too.