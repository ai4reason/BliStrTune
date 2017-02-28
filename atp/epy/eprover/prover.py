import sys
import hashlib
import commands
import json
from os.path import join
from datetime import datetime

from .. import ATP_ROOT, failed
from result import Result
import parallel

E_RUN_ARGS = "--cpu-limit=%s --output-level=0 --resources-info --memory-limit=1024 --print-statistics --tstp-format "

def getresult(args, out=None, samples=False):
   output = commands.getoutput("time -p eprover %s" % args)
   if out: out.write(output)
   result = Result(output, samples=samples)
   if not out and "STATUS" not in result:
      failed("\n%s: prover.py: failed eprover %s\n" % (str(datetime.now()),args))
      failed(output)
   return result

def run(proto, problem, limit, out=None, samples=False):
   f_problem = join(ATP_ROOT, "benchmarks", problem)
   args = (E_RUN_ARGS % limit)+(" --training-examples=3 " if samples else "")
   args += proto+" "+f_problem
   result = getresult(args, out=out, samples=samples)
   result["TIME_LIMIT"] = limit
   return result

def run_parallel(proto, problems, limit, cores=4, samples=False):
   return parallel.parallel_proto(proto, problems, limit, cores=cores, samples=samples)

