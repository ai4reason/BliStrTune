#!/usr/bin/python

from sys import argv
from os import getenv

from epy.eprover import scheduler
from epy.expres import update

CORES = int(getenv("CORES", 32))

def run(sid, bid, limit):
   "Run benchmarks, update summary, and create HTML."
   print "SCHEDULER %s @ %s @ %s" % (sid,bid,limit)
   results = scheduler.run_parallel(sid, bid, limit, cores=CORES)
   update.update_sid(sid, bid, limit, "e", results)
   print 

if len(argv) != 4:
   print "usage: %s sid bid limit" % argv[0]
   print "  eg.: %s auto-schedule bushy 5" % argv[0]
else:
   run(argv[1], argv[2], int(argv[3]))

