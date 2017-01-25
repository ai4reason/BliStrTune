#!/usr/bin/python

import sys
import re
from epy import eprover
from epy import epymils
from os import getenv

RESULT="Result for ParamILS: %(STATUS)s, %(USER_TIME)s, %(PROCESSED)s, 1000000, %(SEED)s"

def make_params_argv():
   params = {}
   i = 6
   while i < len(sys.argv):
      params[sys.argv[i].lstrip("-")] = sys.argv[i+1]
      i += 2
   return params

def update_result(result, params, seed):
   result["SEED"] = seed
   if result["STATUS"] in eprover.STATUS_OUT+["CounterSatisfiable"]:
      if "USER_TIME" in result: del result["USER_TIME"]
      if "PROCESSED" in result: del result["PROCESSED"]
   if not "USER_TIME" in result:
      result["USER_TIME"] = 100 
   if not "PROCESSED" in result:
      result["PROCESSED"] = 1000000 

def run():
   limit = int(float(sys.argv[3]))
   problem = sys.argv[1]
   seed = sys.argv[5]
   params = make_params_argv()
   
   print "running eprover: %s" % problem

   proto= epymils.e_proto(params)
   result = eprover.prover.run(proto, problem, limit)
   update_result(result, params, seed)
   print RESULT % result

if len(sys.argv) < 2:
   print "usage: %s instance spec time cutoff seed arg1 val1 ..." % sys.argv[0]
else:
   run()

