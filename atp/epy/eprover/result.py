import re
from . import STATUS_OK

INFOS = {
   "PROCESSED": "Processed clauses",
   "GENERATED": "Generated clauses",
   "INITIAL":   "Initial clauses",
   "AXIOMS":    "Parsed axioms",
   "_USER_TIME": "User time",
   "SINE_PRUNED": "Removed by relevancy pruning/SinE",
}

SUM = [ "PROCESSED", "GENERATED", "USER_TIME", "SINE_PRUNED" ]

PATS = {key:re.compile(r"# %s\s*: (\S*)" % INFOS[key]) for key in INFOS}
PATS["STATUS"] = re.compile(r"# SZS status (\S*)")
PATS["USER_TIME"] = re.compile("user (\d*\.\d*)")

def type_val(strval):
   if strval.isdigit():
      return int(strval)
   if strval.find(".") >= 0:
      try:
         return float(strval)
      except:
         pass
   return strval

class Result(dict):
   def __init__(self, output=None, result=None):
      if output:
         self.parse(output)
      if result:
         dict.update(self, result)

   def parse(self, output):
      for line in output.split("\n"):
         for pat in PATS:
            mo = PATS[pat].search(line)
            if mo:
               self.update(pat, type_val(mo.group(1)))
      if "_USER_TIME" in self:
         self["USER_TIME"] = self["_USER_TIME"]
         del self["_USER_TIME"]
      return self

   def update(self, name, val):
      if name in self and name in SUM:
         self[name] += val
      else:
         self[name] = val # keep the last value

   def solved(result, limit=None):
      ok = "STATUS" in result and result["STATUS"] in STATUS_OK
      if limit:
         return ok and result["USER_TIME"] <= limit
      return ok

   def limit(result):
      return result["TIME_LIMIT"]

