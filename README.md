# QM-1100
This repo includes scripts and instructions to program QM1100 Pick and Place Machine manufactured by SMT Max. We used these scripts to protoypes Ubo PCBs and wanted to share them with maker community.

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

To acccomplish this. Please make sure the units are in mm (milimeters).

![alt text](https://github.com/ubopod/QM1100/blob/main/images/export_mnt.png?raw=true)

2. Setup the feeder file

We need to tell the machine on which feeder is each component mounted and provide some meta data on each feeder. This part needs to be done manually

3. calculating the rotation angle

This is a tricky part that requires some geometic imagination. Orientation of the part on the feeder and orientation of the board, as well as rotation direction (CW/CCW) of the machine picking head.  
