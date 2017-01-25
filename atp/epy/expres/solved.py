from os import listdir
from os.path import join, isfile
import json

from .. import ATP_ROOT, mkdir
from ..eprover import benchmark

class Solved:
   def __init__(self, prefix, bid, limit, prover="e"):
      self.prefix = prefix
      self.bid = bid
      self.limit = limit
      self.prover = prover
      self.f_solved = join(ATP_ROOT, "results", prover, "solved-%s-%s-%ss.json" % (prefix,bid,limit))
      self.solvedb = self.load()
      self.index = self.solvedb[0] # never delete from index, only add!
      self.data = self.solvedb[1]

   def __repr__(self):
      return str((self.index, self.data))

   def load(self):
      return json.load(file(self.f_solved)) if isfile(self.f_solved) else ([],{})

   def save(self):
      mkdir(self.f_solved)
      json.dump(self.solvedb, file(self.f_solved,"w"))

   def get(self, pid):
      if pid not in self.data:
         return set([])
      mask = self.data[pid]
      return frozenset([p for (i,p) in enumerate(self.index) if mask&2**i])

   def put(self, pid, problems):
      new = set(problems).difference(self.index)
      self.index.extend(new)
      ind = {p:i for (i,p) in enumerate(self.index)}
      mask = reduce(lambda m,p:m|2**ind[p],problems,0L)
      self.data[pid] = mask

   def update(self, pid, problems):
      self.put(pid, set(problems).union(self.get(pid)))
      self.save()

   def solvers(self):
      ":: self -> dict(problem -> [prover])"
      problems = benchmark.problems(self.bid)
      _solvers = {p:set([]) for p in problems}
      for pid in self.data:
         pidsolved = self.get(pid)
         for p in problems:
            if p in pidsolved:
               _solvers[p].add(pid)
      return _solvers

def limits(prefix, bid, prover="e"):
   files = listdir(join(ATP_ROOT, "results", prover))
   beg = "solved-%s-%s-" % (prefix, bid)
   return [int(x[len(beg):-6]) for x in files if x.startswith(beg) and x.endswith("s.json")]

