#!/usr/bin/python

import sys
from epy import epymils

def make_params(init):
   params = {}
   i = 0
   while i < len(init):
      try:
         params[init[i]] = init[i+1]
      except:
         raise Exception(str(init))
      i += 2
   return params

def run():
   init = file(sys.argv[1]).read().rstrip().split(" ")
   params = make_params(init)
   proto = epymils.e_proto(params)
   sys.stdout.write(proto)
   
run()

