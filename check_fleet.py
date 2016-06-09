#!/bin/python -B

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--unit", help="Defines units which have to checked")
args = parser.parse_args()

if args.unit:
  unit_string = args.unit

exit_code = 0

command = 'fleetctl --endpoint "http://coreos01:4001,http://coreos02:4001,http://coreos03:4001" list-units --full -no-legend | grep %s' % unit_string

units = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

for unit in iter(units.stdout.readline, ''):
  unit_props = unit.split()
  unit = unit_props[0]
  active = unit_props[2]
  sub = unit_props[3]

  if active == "active":
    if sub == "running":
      print "OK: Unit %s is running." % unit
      if 0 == exit_code:
        exit_code = 0
    else:
      print "WARNING: Unit %s is %s." % (unit, sub)
      if 1 > exit_code:
        exit_code = 1
  elif active == "inactive":
    print "CRITICAL: Unit %s is %s with state \"%s\"." % (unit, active, sub)
    exit_code = 2
  elif active == "failed":
    print "CRITICAL: Unit %s failed with state \"%s\"." % (unit, sub)
    exit_code = 2
  else:
    print "CRITICAL: Unit %s is %s with state \"%s\"." % (unit, active, sub)
    exit_code = 2

exit(exit_code)
