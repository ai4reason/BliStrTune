#!/usr/bin/python

import sys
import re
import json
from os import getenv

from epy import eprover
from epy import epymils

RESULT="Result for ParamILS: %(STATUS)s, %(USER_TIME)s, %(PROCESSED)s, 1000000, %(SEED)s"

def make_params_argv():
   params = {}
   i = 6+1
   while i < len(sys.argv):
      params[sys.argv[i].lstrip("-")] = sys.argv[i+1]
      i += 2
   return params

def update_result(result, seed):
   result["SEED"] = seed
   if result["STATUS"] in eprover.STATUS_OUT+["CounterSatisfiable"]:
      if "USER_TIME" in result: del result["USER_TIME"]
      if "PROCESSED" in result: del result["PROCESSED"]
   if not "USER_TIME" in result:
      result["USER_TIME"] = 100 
   if not "PROCESSED" in result:
      result["PROCESSED"] = 1000000 

def run():
   global_params = json.loads(sys.argv[1])
   limit = int(float(sys.argv[3+1]))
   problem = sys.argv[1+1]
   seed = sys.argv[5+1]
   
   tunes_params = make_params_argv()
   epymils.params_update_finetunes(global_params, tunes_params)

   print "running eprover: %s" % problem

   proto = epymils.e_proto(global_params)
   print "proto: ", proto
   result = eprover.prover.run(proto, problem, limit)
   update_result(result, seed)
   print RESULT % result

if len(sys.argv) < 2:
   print "usage: %s JSON instance spec time cutoff seed arg1 val1 ..." % sys.argv[0]
else:
   run()

