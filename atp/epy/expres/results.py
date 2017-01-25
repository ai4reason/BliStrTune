from os import system
from os.path import join, dirname, relpath, isfile, split
import json

from .. import ATP_ROOT, mkdir
from ..eprover import Result, protocol

class Results(dict):
   def __init__(self, f_results):
      self.f_results = f_results
      self.load()

   def load(self): 
      self.clear()
      if isfile(self.f_results):
         results = json.load(file(self.f_results))
         results = {x:Result(result=results[x]) for x in results}
         dict.update(self, results)

   def save(self):
      mkdir(self.f_results)
      json.dump(self, file(self.f_results,"w"), indent=3)
   
   def update(self, new): # new :: {problem:Result}
      for problem in new:
         if problem not in self:
            self[problem] = new[problem]
         else:
            self[problem] = max(self[problem], new[problem], key=Result.limit)
      self.save()

class PidResults(Results):
   def __init__(self, pid, prover="e"):
      f_results = join(ATP_ROOT, "results", prover, "protos", pid+".json")
      if not isfile(f_results):
         self.create(pid, f_results, prover)
      Results.__init__(self, f_results)
      self.pid = pid

   def create(self, pid, f_results, prover):
      hash = protocol.hash(pid)
      # create an empty hashed results file for pid
      f_hash = join(ATP_ROOT, "results", prover, "protos", "_epy", 
         hash[0:3], hash[3:6], "epy_%s.json"%hash)
      if not isfile(f_hash):
         mkdir(f_hash)
         file(f_hash,"w").write("{}")
      # link the hashed results
      (d_link, link) = split(f_results)
      rel = relpath(f_hash, d_link)
      mkdir(f_results)
      system("cd %s; ln -s %s %s 2> /dev/null" % (d_link, rel, link))
      
class SidResults(Results):
   def __init__(self, sid, prover="e"):
      f_results = join(ATP_ROOT, "results", prover, "scheds", sid+".json")
      Results.__init__(self, f_results)      
      self.sid = sid

