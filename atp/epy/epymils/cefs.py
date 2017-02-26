from os import getenv
from os.path import join
from itertools import cycle
import json

from .params import Domain, cef2block

GLOBAL_CEFS = join(getenv("ATP_ROOT", join(getenv("HOME"), "atp")), "CEFS.json")

def load():
   "{int:cef}"
   return json.load(file(GLOBAL_CEFS))

def save(cefs):
   "{int:cef} -> None"
   json.dump(cefs, file(GLOBAL_CEFS,"w"), indent=3, sort_keys=True)

def weight(cef):
   return cef.split("(")[0]

def weight_bests(weight, cefs):
   weight_cefs = [cef for cef in cefs if cef.startswith(weight+"(")]
   usage = sum([cefs[cef] for cef in weight_cefs])
   bests = sorted([(cefs[cef],cef) for cef in weight_cefs],reverse=True)
   return (usage, bests)

def bests(count=50, cefs=None):
   if not cefs:
      cefs = load()

   ret = []
   weights = set(map(weight,cefs))
   w_bests = sorted([weight_bests(w,cefs) for w in weights],reverse=True)
   count = min(len(cefs), count)

   for (usage,bests) in cycle(w_bests):
      if len(ret) >= count:
         return Domain(*map(cef2block,ret[:count]))
      if bests:
         cef = bests.pop(0)[1]
         ret.append(cef)

def used(cef):
   "Increase the usage counter for the given CEF"
   cefs = load()
   # TODO: locking
   cefs[cef] = cefs[cef]+1 if cef in cefs else 1
   save(cefs)

