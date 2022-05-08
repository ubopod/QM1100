# QM-1100 Pick and Place Setup Guide
This repo includes scripts and instructions to program QM1100 Pick and Place Machine manufactured by SMT Max. We used these scripts to protoypes Ubo top PCB and wanted to share them with maker community.

[[WORK IN PROGRESS]]

## Overview

In order to prepare the Pick and Plance (PnP) machine, several steps must be taken. We will walk you through these steps below:

### 1. Export mounting coordinate file from Eagle:

The first step is to export the mounting file from Eagle in the following format:

```
C1 45.99 105.42 180 10uF 0805-NO
C2 55.71 97.50 270 10uF 0805-NO
C3 51.19 101.13  90 0.1uF 0603-NO
...
```

To acccomplish this, go to ` File > Export > Mount SMD` in your board/layout window (See image below).

Please make sure the units are in mm (milimeters).The unit will follow the unit you have set in your layout grid. 

![alt text](https://github.com/ubopod/QM1100/blob/main/images/export_mnt.png?raw=true)

The export operation will give you two files, one for top side components and another for bottom side components. Since our design is one-sides and the machine only support single-sided placement, we will ignore the bottom `.mnt` file.

### 2. Setup the feeder file

We need to tell the machine on which feeder each component is mounted and provide some meta data on each feeder. This part needs to be prepare manually. Here is an example of the CSV format for this file:

```
# feeder_id angle value package z-height vision file skip pause note IC
38 90 Ferrite 0805-NO 700 No “””no””” No 0 None No
39 90 33pF 0603-NO 700 No “””no””” No 0 None No
40 90 100pF 0603-NO 700 No “””no””” No 0 None No
...
```

Here's a short description of each value on each column: 

  1. Feeder ID number 
  2. Part orientation in degrees on the feeder (must be calcuated by user)
  3. Component name/value as it appears on the Eagle mounting list (.mnt file)
  4. Component package it appears on the Eagle mounting list (.mnt file)
  5. Component z-axis height in machine units; 700 is the default but for taller parts it must be adjusted. Please a look at machine manual for more info.
  6. QM Vision enabled for this component. Default is No. If you wish to set up vision, consult with manual and change to Yes.
  7. Path to Vision file. Default is “””no””” if QM Vision is not selected.
  8. Whether to skip placing components on this feeder. Default is No.
  9. Pause time before attampting to pick component from tray. Default is 0 seconds.
  10. Notes regarding components on feader. Default is None.
  11. Whether the component is an IC. Default is No.
  12. Calculating the rotation angle

This can be a tricky to detemine feeder angle and it requires some geometic imagination. 

It is basically the amount of rotation (Clock Wise) that the pickup nozzle must make after it picks up the part from the feeder to place it with correct orientaton on the board. The orientation for passive components such as resistors and ceramin capacitors can be offset by 180 degree and still not cause any problems electrically. 

However, orientation of diodes, LEDS, ICS, etc must be calculated with care. The positional angle of parts on PCB is calcuated by EAGLE (included in the .mnt file) based on a cartesian coordiate with an origin marketed with cross sign on the board layout. 

Basically the amount of rotation nozzle must make to correctly place a part after it picks it up from the feeder can be calculated as:

```
Head rotation angle = ( part angle position on the feer - part angle of position on PCB ) % 360
```

The best way derive part angle for each feer is to imagin picking that component by hand and having to rotate it clockwise before placing it on the board and imagine the amount of rotation needed to place it correctly on the PCB for a given part on PCB coming from the target feeder. This feed this number on the left hand side of the above formula and also add part angle from .mnt file into the formula and calculate part angle on feeder. You can re-try this for different parts from the same feeder to make sure formula gives you the right amount of rotation based on the value derived for the first component (place note that the part feeder angle is a constant and works like and offset value for all parts coming from that feeder).

### 4. run script

In order to generate the part list to prgram the machine with

```
python3 qm1100_v2.py <feeders.csv> <smd_mounting_coord.mnt> <output.csv> pcb_orientation_degrees
```

The formula takes comma seperated feeder list as the first argument, mounting coordinates list exported from eagle, and outputs parts list that includes all parts, placement coordinates in machine unit, correct amount of rotation for each part, etc. This list will then uploaded to the machine along with feeder list to configure it.


| Orientation on the machine| Orientation in Eagle |
| ------------- | ------------- |
| ![alt text](https://github.com/ubopod/QM1100/blob/main/images/pnp_pcb_orientation.png?raw=true)  | ![alt text](https://github.com/ubopod/QM1100/blob/main/images/eagle_pcb_orientation.png?raw=true) |

### 5. inspect the output parts file
### 6. program the machine 
#### 6.1. upload feeder file
#### 6.2. upload parts file 
#### 6.3. set board offset
