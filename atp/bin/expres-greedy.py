#!/usr/bin/python

from sys import argv

from epy.eprover import benchmark
from epy.expres import Solved

PROVER = "e"

def remove(solved, problems):
   for pid in solved:
      solved[pid] = solved[pid].difference(problems)

def best(solved):
   return max([(len(solved[pid]),pid) for pid in solved])

def run(bid, limit, selector):
   problems = set(benchmark.problems(bid))
   solved = Solved("protos", bid, limit, PROVER)
   solved = {pid:set(solved.get(pid)) for pid in solved.data if selector in pid}

   total=0
   m=len(problems)
   n=0
   while m>0:
      (l,a) = best(solved)
      if l == 0:
         break
      m -= l
      n += 1
      total += l
      done = solved[a]
      print "%s: solved %d, remains %d" % (a,l,m)
      remove(solved,done)
   
   print
   print "SOLVED: %d" % total
   print "COUNT: %d" % n

if len(argv) < 3:
   print "usage: %s bid limit [selector]" % argv[0]
else:
   run(argv[1], int(argv[2]), argv[3] if len(argv)>3 else "")

