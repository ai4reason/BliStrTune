import hashlib
from os import walk
from os.path import join, relpath

from .. import ATP_ROOT, mkdir
import prover
import parallel
import benchmark

def pid_path(pid):
   return join(ATP_ROOT, "protos", pid)

def hash_path(hash):
   return join(ATP_ROOT, "protos", "_epy", 
      hash[0:3], hash[3:6], "epy_%s.proto"%hash)

def proto_hash(proto):
   norm = proto.replace("'","").replace('"',"")
   norm = sorted(norm.split(" "))
   norm = "".join(norm)
   return hashlib.sha1(norm).hexdigest()

def hash(pid):
   return proto_hash(load(pid))

def load(pid):
   return file(pid_path(pid)).read().strip()

def register(pid, proto):
   hash = proto_hash(proto)
   mkdir(pid_path(pid))
   mkdir(hash_path(hash))
   file(pid_path(pid),"w").write(proto)
   file(hash_path(hash),"w").write(proto)

def known_pids():
   d_proto = join(ATP_ROOT, "protos")
   ret = [join(d,f) for (d,ds,fs) in walk(d_proto) if "_epy" not in d for f in fs]
   return sorted([relpath(x,d_proto) for x in ret])

def run(pid, problem, limit, out=None):
   return prover.run(load(pid), problem, limit, out=out)

def run_parallel(pid, bid, limit, cores=4):
   problems = benchmark.problems(bid)
   return parallel.parallel_pid(pid, problems, limit, cores=cores)

