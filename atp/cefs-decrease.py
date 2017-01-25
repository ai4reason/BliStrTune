#!/usr/bin/python

import sys
import json

def decrease(cefs):
   for key in cefs:
      cefs[key] -= 1
   map(cefs.__delitem__, [x for x in cefs if cefs[x]==0])


if len(sys.argv) != 2:
   print "usage: %s CEFS.json" % sys.argv[0]
   print "use to: decrease all values in CEFS dictionary by one"
   sys.exit()

cefs = json.load(file(sys.argv[1]))

decrease(cefs)

print json.dumps(cefs, indent=3, sort_keys=True)

