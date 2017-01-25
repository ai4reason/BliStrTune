# vim: set fileencoding=utf8 :

from os.path import join, isfile
import json

from .. import ATP_ROOT
from ..eprover import benchmark, protocol
from solved import Solved

class Summary(dict):
   def __init__(self, prefix, bid, limit):
      self.prefix = prefix
      self.bid = bid
      self.limit = limit
      self.load()
      self._solved = None

   def load(self):
      f_json = "%s-%s-%ss.json" % (self.prefix,self.bid,self.limit)
      self.f_summary = join(ATP_ROOT, "results", f_json)
      data = json.load(file(self.f_summary)) if isfile(self.f_summary) else {}
      dict.update(self, data)

   def save(self):
      json.dump(self, file(self.f_summary,"w"), indent=3, sort_keys=True)

   def update(self, pid, prover, results):
      problems = benchmark.problems(self.bid)
      done = [x for x in results if results[x].limit() >= self.limit and x in problems]
      solved = [x for x in done if results[x].solved(self.limit)]
      total = len(done)

      sum = {}
      sum["TOTAL"] = total
      sum["SOLVED"] = len(solved)
      sum["ERRORS"] = len(problems) - len(done)
      sum["%"] = 100.0 * (len(solved) / float(len(problems)))

      self[prover+"~"+pid] = sum
      self.save()
      return self

   def compute_sotacs(self):
      solved = Solved(self.prefix,self.bid,self.limit,"e") # TODO: any prover
      solvers = solved.solvers()
      sotac = {p:(1.0/len(solvers[p]) if len(solvers[p])>0 else 0) for p in solvers}

      for id in self:
         (prover, pid) = id.split("~")
         if prover != "e": 
            print "Warning: Unsupported prover '%s'. Skipped." % prover
            self[id]["SOTAC"] = 0
            self[id]["E-SOTAC"] = 0
            continue # TODO: any prover

         pidsolved = solved.get(pid)
         e_sotac = sum([sotac[p] for p in pidsolved])
         c_sotac = e_sotac / len(pidsolved) if len(pidsolved)>0 else 0

         self[id]["SOTAC"] = c_sotac
         self[id]["E-SOTAC"] = e_sotac

   def table(self, usehash=False, usesotacs=True):
      "Convert summary to a table suitable for HTML-ization"
      if usehash:
         HEADER = ["PROVER","HASH","SOLVED","TOTAL","ERRORS","%"]
      else:
         HEADER = ["PROVER","SOLVED","TOTAL","ERRORS","%"]
      if usesotacs:
         self.compute_sotacs()
         HEADER.extend(["SOTAC","E-SOTAC"])

      data = []
      for id in self:
         pid = id.split("~")[1]
         if usehash:
            hash = protocol.hash(pid)
            row = [id,hash[:3]+"..."+hash[-3:]]
         else:
            row = [id]
         for key in HEADER[2 if usehash else 1:]:
            row.append(self[id][key] if key in self[id] else "err")
         data.append(row)

      table = {}
      table["HEADER"] = HEADER
      table["CLASSES"] = {}
      table["DATA"] = data
      return table

