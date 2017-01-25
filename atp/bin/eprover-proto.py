#!/usr/bin/python

from sys import argv
from os import getenv

from epy.eprover import protocol
from epy.expres import update

CORES = int(getenv("CORES", 32))

def run(pid, bid, limit):
   "Run benchmarks, update summary, and create HTML."
   print "PROTOCOL %s @ %s @ %s" % (pid, bid, limit)
   results = protocol.run_parallel(pid, bid, limit, cores=CORES)
   update.update_pid(pid, bid, limit, "e", results)
   print

if len(argv) != 4:
   print "usage: %s pid bid limit" % argv[0]
   print "  eg.: %s auto-schedule bushy 5" % argv[0]
else:
   run(argv[1], argv[2], int(argv[3]))

#run("auto-schedule", "test", 5)

