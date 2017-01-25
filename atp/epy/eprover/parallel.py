from multiprocessing import Pool
import sys
from os.path import join

import benchmark
import protocol
import scheduler

OUT = sys.stdout

def _run_pid(arg):
   result = protocol.run(arg[0], arg[1], arg[2])
   report(result)
   return result

def _run_sid(arg):
   result = scheduler.run(arg[0], arg[1], arg[2])
   report(result)
   return result

def report(result):
   if OUT:
      OUT.write("." if result.solved() else "!")
      OUT.flush()

def parallel(wrapper, id, problems, limit, cores=4):
   n = len(problems)
   pool = Pool(cores)
   args = zip([id]*n,problems,[limit]*n) 
   results = pool.map(wrapper, args)
   return {x:y for (x,y) in zip(problems, results)}

def parallel_pid(pid, problems, limit, cores=4):
   return parallel(_run_pid, pid, problems, limit, cores)

def parallel_sid(sid, problems, limit, cores=4):
   return parallel(_run_sid, sid, problems, limit, cores)


