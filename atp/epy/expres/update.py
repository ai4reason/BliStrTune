from results import PidResults, SidResults
from solved import Solved, limits
from summary import Summary
import html

def update_pid(pid, bid, limit, prover, results, dohtml=True):
   PidResults(pid,prover).update(results)
   solved = [x for x in results if results[x].solved(limit)]
   Solved("protos",bid,limit,prover).update(pid,solved)
   summary = Summary("protos",bid,limit).update(pid,prover,results)
   if dohtml: html.create_summary("protos",bid,limit,summary,usehash=True)
   # additionally update data for lower available time limits
   for lim in limits("protos",bid,prover):
      if lim < limit:
         solved = [x for x in results if results[x].solved(lim)]
         Solved("protos",bid,lim,prover).update(pid,solved)
         summary = Summary("protos",bid,lim).update(pid,prover,results)
         if dohtml: html.create_summary("protos",bid,lim,summary,usehash=True)

def update_sid(sid, bid, limit, prover, results, dohtml=True):
   SidResults(sid,prover).update(results)
   solved = [x for x in results if results[x].solved(limit)]
   Solved("scheds",bid,limit,prover).update(sid,solved)
   summary = Summary("scheds",bid,limit).update(sid,prover,results)
   if dohtml: html.create_summary("scheds",bid,limit,summary)

