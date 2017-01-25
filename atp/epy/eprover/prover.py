import hashlib
import commands
import json
from os.path import join

from .. import ATP_ROOT
from result import Result

E_RUN_ARGS = "--cpu-limit=%s --output-level=0 --resources-info --memory-limit=1024 --print-statistics --tstp-format "

def getresult(args, out=None):
   output = commands.getoutput("time -p eprover %s" % args)
   if out: out.write(output)
   return Result(output)

def run(proto, problem, limit, out=None):
   f_problem = join(ATP_ROOT, "benchmarks", problem)
   result = getresult((E_RUN_ARGS % limit)+proto+" "+f_problem,out=out)
   result["TIME_LIMIT"] = limit
   return result

