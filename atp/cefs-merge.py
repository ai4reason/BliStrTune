#!/usr/bin/python

import sys
import json

def merge(map1,map2):
   ret = {key:0 for key in set().union(map1, map2)}
   for key1 in map1:
      ret[key1] += map1[key1]
   for key2 in map2:
      ret[key2] += map2[key2]
   return ret

if len(sys.argv) != 3:
   print "usage: %s CEFS1.json CEFS2.json" % sys.argv[0]
   print "use to: merge two CEF files
   sys.exit()

cefs1 = json.load(file(sys.argv[1]))
cefs2 = json.load(file(sys.argv[2]))

cefs = merge(cefs1, cefs2)

print json.dumps(cefs, indent=3, sort_keys=True)

