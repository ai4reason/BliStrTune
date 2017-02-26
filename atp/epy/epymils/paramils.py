import sys
import os
from os.path import join
import subprocess
import json
import math

from .log import *
from .data import *
from .params import *
from .scenario import *
from .setting import *

def params_clean(params):
   """Remove unused slots from params
   
   This is, however, not usually done, because unused parameters can become 
   used again and their values are set to defaults, possibly reseting 
   usefull values.
   """

   if not "slots" in params:
      return
   slots = int(params["slots"])
   delete = []
   for param in params:
      if param.startswith("freq") or param.startswith("cef"):
         n = int(param.lstrip("freqcef"))
         if n >= slots:
            delete.append(param)
   for param in delete:
      del params[param]

def params_best(outdir, select_index=-1):
   """Read ParamILS output and return the best result in format {arg:val}.

   Best result is the one with highest problem count and lowest quality.
   Consider results of several ParamILS runs.
   Return also raw ParamILS data (with time, quality, etc.).
   Optionally use index to select solution of each run (the are
   reported with descresing quality, so the last is the best;
   first is the input configuration).
   """

   fs = [f for f in os.listdir(outdir) if "traj" in f and f.endswith(".txt")]
   rs = [file(join(outdir,f)).readlines()[select_index].strip().split(",") for f in fs]
   if not rs:
      return (None, None)
   best = min(rs, key=lambda r: (-int(r[2]),float(r[1])))
   params = [p.split("=") for p in best[5:]]
   params = {p[0].strip():p[1].strip("' ") for p in params}

   #params_clean(params)
   return (params, best)

def params_better(info1, info2):
   if not info2:
      return True
   better = min(info1, info2, key=lambda r: (-int(r[2]),float(r[1])))
   return info1 is better

def run_paramils(scenariofile, binary="./param_ils_2_3_run.rb", count=1, N="100", validN="800", init="1", out=None):
   """Run several instances of ParamILS in parallel on the same scenario.

   Return the list of exit codes (zeros on success).
   """

   def make_args(numRun):
      return [binary, "-numRun", numRun, "-scenariofile", scenariofile, "-N", N,"-validN", validN, "-init", init, "-output_level", "0", "-userunlog", "0"]
   if not out:
      out = open(os.devnull, 'w')
   args = [make_args(str(n)) for n in range(count)]
   #ps = [subprocess.Popen(arg,stdout=out,close_fds=True,stderr=subprocess.STDOUT) for arg in args]
   ps = [subprocess.Popen(arg,stdout=out,close_fds=True) for arg in args]
   #ps = [subprocess.Popen(arg) for arg in args]
   rets = [p.wait() for p in ps]
   if 1 in rets:
      sys.stdout.write("ERROR: Running paramils (return codes) %s\n" % str(rets))
   return rets

def run_globaltune(iter_global, cefs, defaults=None, out=None):
   "Run global-tuning phase"

   d_global = "iter-%02d-A-global" % iter_global
   log("\nGLOBAL_TUNE %s" % d_global)
   if os.path.exists(d_global):
      os.system("rm -fr %s" % d_global)
   os.system("mkdir -p %s" % d_global)

   params = params_globaltune(SLOTS, cefs)
   if defaults:
      params_set_default(params, defaults)

   scenario = scenario_globaltune(CUTOFF, TIMEOUT_GLOBAL, 
      d_global, INSTANCE_FILE, bin="../../epymils_globaltune.py")

   f_params = join(d_global, "params.txt")
   f_scenario = join(d_global, "scenario.txt")
   d_output = join(d_global, "paramils-out")

   log("Space size: 10^%.2f\n" % math.log(params_size(params),10))
   file(f_params,"w").write(str(params))
   file(f_scenario,"w").write(scenario)
   
   if out is True:
      out = file(join(d_global,"paramils.out"),"w")
   run_paramils(f_scenario,count=CORES,N=PROBLEMS,validN="0",init="1" if defaults else "0",out=out)
   (in_params, in_info) = params_best(d_output, select_index=1)
   (out_params, out_info) = params_best(d_output)

   log_params(in_params, "IN:")
   log_params(out_params, "OUT:")
   log("\nQ OUT:", ["T = %ss Q =%s # =%s" % (int(float(out_info[0])),out_info[1],out_info[2])])
   log_proto("iter-%02d-A-global-in"%iter_global, in_params)
   log_proto("iter-%02d-A-global-out"%iter_global, out_params)

   #print "Best: ", params
   return (out_params, out_info)

def run_finetune(iter_global, cefs, params, out=None):
   "Run fine-tuning phase"

   params = dict(params)
   d_finetune = "iter-%02d-B-finetune" % iter_global
   log("\nFINE_TUNES %s" % d_finetune)
   if os.path.exists(d_finetune):
      os.system("rm -fr %s" % d_finetune)
   os.makedirs(d_finetune)

   tune_params = params_finetune(params)
   parstr = repr(json.dumps(params))
   scenario = scenario_finetune(parstr, CUTOFF, TIMEOUT_FINETUNES, d_finetune,
      INSTANCE_FILE, bin="../../epymils_finetune.py")

   f_params = join(d_finetune, "params.txt")
   f_scenario = join(d_finetune, "scenario.txt")
   d_output = join(d_finetune, "paramils-out")

   log("Space size: 10^%.2f\n" % math.log(params_size(tune_params),10))
   file(f_params,"w").write(str(tune_params))
   file(f_scenario,"w").write(scenario)

   if out is True:
      out = file(join(d_finetune,"paramils.out"),"w")
   run_paramils(f_scenario,count=CORES,N=PROBLEMS,validN="0",init="1",out=out)
   (best_params, best_info) = params_best(d_output)

   log_proto("iter-%02d-B-fintetune-in"%iter_global, params)
   changes = params_update_finetune(params, best_params)
   for old in changes:
      index = cefs.index(old)
      cefs[index] = changes[old]
      log(">>>>\t[%2d] %s ---> %s" % (index,block2cef(old),block2cef(changes[old])))
   if not changes:
      log(">>>>\tNo improvement!")
   log("\nQ OUT:", ["T = %ss Q =%s # =%s" % (int(float(best_info[0])),best_info[1],best_info[2])])

   log_proto("iter-%02d-B-fintetune-out"%iter_global, params)
   
   return (params, best_info)

def run_enigmatune(cefs, params, out=None):
   """Create an Enigma model for 'data/problems.txt' and 
   incorporate Enigma CEF into the current protocol"""

   d_enigmatune = "iter-E-enigmatune" 
   log("\nENIGMA_TUNE")
   if os.path.exists(d_enigmatune):
      os.system("rm -fr %s" % d_enigmatune)
   os.makedirs(d_enigmatune)
  
   # make ENIGMA model
   args = eprover.prover.E_RUN_ARGS % CUTOFF
   args += epymils.e_proto(params)
   system("./enigma-problems-model.sh %s" % args)

   ####print str(epymils.params_finetunes(defaults))
   enigma_params = epymils.params_enigmatune(params)
   parstr = repr(json.dumps(params))
   scenario = epymils.scenario_enigmatune(parstr, CUTOFF, 
      TIMEOUT_ENIGMATUNES, d_enigmatune,
      INSTANCE_FILE, bin="../../epymils_enigmatune.py")

   f_params = join(d_enigmatune, "params.txt")
   f_scenario = join(d_enigmatune, "scenario.txt")
   d_output = join(d_enigmatune, "paramils-out")

   file(f_params,"w").write(str(enigma_params))
   file(f_scenario,"w").write(scenario)

   if out is True:
      out = file(join(d_enigmatune,"paramils.out"),"w")
   epymils.run_paramils(f_scenario,count=CORES,N=PROBLEMS,validN="0",init="1",out=out)
   (params_best, best_info) = epymils.params_best(d_output)

   ###log_proto("iter-%02d-C-fintetunes-in"%iter_global, params)
   ###changes = epymils.params_update_finetunes(params, params_best)
   ###for old in changes:
   ###   index = cefs.index(old)
   ###   cefs[index] = changes[old]
   ###   log(">>>>\t[%2d] %s ---> %s" % (index,epymils.block2cef(old),epymils.block2cef(changes[old])))
   ###if not changes:
   ###   log(">>>>\tNo improvement!")

   epymils.params_update_enigmatune(params, params_best)
   log_proto("iter-E-enigmatune-out", params)
   log_params(params, "OUT:")

   return (params, best_info)
   
