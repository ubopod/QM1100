#!/usr/bin/env python
#
# QM1100
# Change exported part list from Eagle to match provided feeder list/definition loaded on QM1100 Machine
#
# Copyright (c) 2021 Mehrdad Majzoobi
# Released under MIT license

import csv
import sys
import codecs
from collections import namedtuple


def parse_parts_file(filename):
    """Parse a file with CSV format and return an object containing
    the stack and part definitions"""
    # Create return object
    part = []
    # Open the CSV file
    with open(filename, 'rb') as csvfile:
        # Create parser and parse every row
        reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'), skipinitialspace=True, delimiter=" ")
        for row in reader:
            # for those components that do not have a value assigned in Eagle
            if len(row) == 5:
                row.insert(4, 'None')
                # print(row)
            PartDef = namedtuple('PartDef', 'part_id x y angle value package')
            p = PartDef._make(row[:6])
            # Add part definition
            part.append(p)
    # Return the parse result
    return part


def parse_feeders_file(filename):
    """Parse a file with CSV format and return an object containing
    the stack and part definitions"""
    # Create return object
    feeder = []
    # Open the CSV file
    with open(filename, 'rb') as csvfile:
        # Create parser and parse every row
        reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'), skipinitialspace=True, delimiter=" ")
        for row in reader:
            FeederDef = namedtuple('FeederDef', 'feeder_id angle value package '
                                 + 'z vision file skip pause note IC')
            f = FeederDef._make(row[:11])
            # Add part definition
            feeder.append(f)
        # Return the parse result
    return feeder

def generate_updated_part(feeder_obj, part_obj):
    updated_part = []
    sequence = 1
    for p in part_obj:
        #rint(p)
        is_on_feeders = False
        for f in feeder_obj:
            #print(f)
            if (p.value == f.value) and (p.package == f.package):
                 is_on_feeders = True
                 # print('Part' + p.index + 'with value + ' ' and package ''+ part matched!')
                 # assign feeder to the part
                 # seq, part_id, x, y, z, a, feeder_id, vision, file,
                 #     skip, pause, note, IC, component
                 PartDef = namedtuple('PartDef', 'part_id x y z angle '
                         + 'feeder_id vision file skip pause note IC component')
                 # Calculate angle by applying stack rotation
                 component = p.value + '-' + p.package
                 # angle = (int(p.angle) + int(f.angle)) % 360
                 angle = (int(f.angle) - int(p.angle))  % 360
                 if angle > 180: angle -= 360
                 a_rotation = (angle/90)*2000
                 x = float(p.x)*2.54*39.3701
                 y = float(p.y)*2.54*39.3701
                 file = p.part_id + ".tif"
                 new_part = [p.part_id, x, y,
                             f.z, a_rotation, f.feeder_id, f.vision, file,
                             f.skip, f.pause, f.note, f.IC, component]
                 new_p = PartDef._make(new_part)
                 sequence = sequence + 1
                 updated_part.append(new_p)
        if is_on_feeders is False:
            continue
            print('part ' + p.part_id + ' is not loaded on any feeder')
    return updated_part

def write_csv_file(csv_file, obj, orientation):
  """Write out the QM100 prt file from the provided object"""
  for part in obj:
      # seq, part_id, x, y, z, a, feeder_id, vision, file,
      #     skip, pause, note, IC, component
      if orientation == "0":
          # if board is placed on the work area with the same exact orientation
          # of eagle or CAD software
          X = "{:.0f}".format(-part.x)
          Y = "{:.0f}".format(-part.y)
      if orientation == "90":
          # if board is placed on the work area with a 90 degree clockwise
          # rotation relative to eagle or CAD software position
          X = "{:.0f}".format(-part.y)
          Y = "{:.0f}".format(part.x)
      if orientation == "-90":
          X = "{:.0f}".format(part.y)
          Y = "{:.0f}".format(-part.x)
      if orientation == "180":
          X = "{:.0f}".format(part.x)
          Y = "{:.0f}".format(part.y)
      A = "{:.0f}".format(part.angle)
      csv_file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (part.part_id,
        X, Y, part.z, A, part.feeder_id, part.vision, part.file, part.skip,
        part.pause, part.note, part.IC, part.component))


  # Check whether we got 3 file name parameters
if len(sys.argv) < 4:
  print("USAGE: python3 qm1100_v2.py <feeders.csv> <parts.csv> <output.csv> -90")
  # python3 qm1100_v2.py Uno_v1.3.2.fds Uno_v1.3_led_topview.mnt Uno_v1.3.2.pts -90")
  # make sure units are in mm for X and Y
else:
  # Load and parse input files
  feeder_obj = parse_feeders_file(sys.argv[1])
  part_obj = parse_parts_file(sys.argv[2])
  orientation = sys.argv[4]
  print(orientation)
  # Process files to generate output
  new_part_obj = generate_updated_part(feeder_obj, part_obj)
  #for p in new_part_obj:
  #  print(p)
  # Write output file
  f = open(sys.argv[3], 'w')
  #f.write("# %s generated by tm245p-merge\n" % sys.argv[3])
  #f.write("# Stacks/boards from %s and parts from %s)\n" %
  #          (sys.argv[1], sys.argv[2]))
  write_csv_file(f, new_part_obj, orientation)
  f.close()
  # Report success
  print("Wrote output file \"%s\"" % sys.argv[3])
