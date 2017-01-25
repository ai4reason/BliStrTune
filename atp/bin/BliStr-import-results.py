#!/usr/bin/python

from sys import argv
from os import listdir 
from os.path import join, basename, abspath

from epy.expres import update, blistr
from epy.eprover import Result, benchmark, protocol, scheduler

PROVER = "e"

def get_results(dir, prot, bid, problems, limit):
   ret = {}
   for p in problems:
      p = p[len(bid)+1:]
      f = join(dir, "allprobs", p+"."+prot)
      p = bid+"/"+p
      ret[p] = Result(file(f).read())
      ret[p]["TIME_LIMIT"] = limit
   return ret

def run(dir, bid, limit):
   problems = benchmark.problems(bid)
   f_out = join(dir, "nohup.out")
   (names,nodes,edges,tops,finals) = blistr.parse_output(file(f_out))
   d_prots = join(dir, "prots")
   name = basename(abspath(dir))

   pids = []
   prots = listdir(d_prots)
   last = prots[-1]
   for prot in prots:
      strat = blistr.strip_proto(prot)
      pid = join(name, names[strat])
      print pid
      if strat in finals:
         pids.append(pid)
     
      protocol.register(pid, file(join(d_prots,prot)).read().strip())
      results = get_results(dir, prot, bid, problems, limit)
      update.update_pid(pid, bid, limit, PROVER, results, dohtml=(prot==last))

   scheduler.register(name+"--final", pids)

if len(argv) != 4:
   print "usage: %s BliStr-dir bid limit" % argv[0]
else:
   run(argv[1], argv[2], int(argv[3]))

