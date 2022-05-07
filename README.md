# QM-1100
This repo includes scripts and instructions to program QM1100 Pick and Place Machine manufactured by SMT Max. We used these scripts to protoypes Ubo PCBs and wanted to share them with maker community.

WORK IN PROGRESS

## Overview

In order to prepare the PnP machine, several steps must be taken. We will walk you through these steps below:

1. Export mounting coordinate file from Eagle:

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

2. Setup the feeder file

We need to tell the machine on which feeder is each component mounted and provide some meta data on each feeder. This part needs to be prepare manually. Heres an example of the CSV format for this file:

```
# feeder_id angle value package z-height vision file skip pause note IC
38 90 Ferrite 0805-NO 700 No “””no””” No 0 None No
39 90 33pF 0603-NO 700 No “””no””” No 0 None No
40 90 100pF 0603-NO 700 No “””no””” No 0 None No
...
```

Here's a short description of each value on each column: 

Column  1. Feeder ID number 

Column  2. part orientation in degrees on the feeder (must be calcuated by user)

Column  3. Component name/value as it appears on the Eagle mounting list (.mnt file)

Column  4. Component package it appears on the Eagle mounting list (.mnt file)

Column  5. Component z-axis height in machine units; 700 is the default but for taller parts it must be adjusted. Please a look at machine manual for more info.

Column  6. QM Vision enabled for this component. Default is No. If you wish to set up vision, consult with manual and change to Yes.

Column  7. Path to Vision file. Default is “””no””” if QM Vision is not selected.

Column  8. Whether to skip placing components on this feeder. Default is No.

Column  9. Pause time before attampting to pick component from tray. Default is 0 seconds.

Column  10. Notes regarding components on feader. Default is None.

Column  11. Whether the component is an IC. Default is No.

3. calculating the rotation angle

This is a tricky part that requires some geometic imagination. Orientation of the part on the feeder and orientation of the board, as well as rotation direction (CW/CCW) of the machine picking head.

Basically the match can be formulated as:

```
Head rotation angle = ( feeder angle - part angle on PCB ) % 360
```

4. run script
5. inspect the output parts file
6. program the machine 
6.1. upload feeder file
6.2. upload parts file 
6.3. set board offset
