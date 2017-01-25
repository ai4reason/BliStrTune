import sys
from os.path import join

from .. import ATP_ROOT

def problems(bid):  
   "Problem list of bid (Benchmark ID, eg. bushy, MZRtrain)"
   f_list = join(ATP_ROOT, "benchmarks", bid+".problems")
   return set(file(f_list).read().rstrip().split("\n"))

