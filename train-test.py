#!/usr/bin/python

from epy.eprover import protocol, prover
import json

proto = file("e.proto").read().strip()
problems = file("data/problems.txt").read().strip().split("\n")

#ret = prover.run(proto, problem[0], 5, samples=True)

ret = prover.run_parallel(proto, problems, 60, cores=4, samples=True)

print ret

