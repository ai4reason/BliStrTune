from os.path import dirname, isdir, join

from .. import ATP_ROOT, mkdir
from result import Result
import protocol
import parallel
import benchmark

def sid_path(sid):
   return join(ATP_ROOT, "scheds", sid)

def load(sid):
   return file(sid_path(sid)).read().strip().split("\n")

def register(sid, pids):
   f_sched = sid_path(sid)
   mkdir(f_sched)
   file(f_sched,"w").write("\n".join(pids))

def scheduling(n, limit):
   l = limit / n
   m = limit % n
   return [l+1]*m + [l]*(n-m)

def run(sid, problem, limit, out=None):
   pids = load(sid)
   time = 0.0
   limits = scheduling(len(pids), limit)

   for (pid,lim) in zip(pids,limits):
      #print "Running %s @ %s @ %ss" % (pid,problem,lim)
      result = protocol.run(pid, problem, lim, out=out)
      time += result["USER_TIME"]
      if result.solved():
         break

   ret = Result()
   ret["USER_TIME"] = time
   ret["STATUS"] = result["STATUS"]
   ret["TIME_LIMIT"] = limit
   return ret

def run_parallel(sid, bid, limit, cores=4):
   problems = benchmark.problems(bid)
   return parallel.parallel_sid(sid, problems, limit, cores=cores)


