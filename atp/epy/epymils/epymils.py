import subprocess
import os
import sys

def cef2block(cef):
    return cef.replace("-","_M_").replace(",","__").replace(".","_D_").replace("(","__").replace(")","")

def block2cef(block):
    parts = block.replace("_M_","-").replace("_D_",".").split("__")
    return "%s(%s)" % (parts[0],  ",".join(parts[1:]))

class List(list):
   def __init__(self, *args):
      super(List,self).__init__(args)

class Arg(List):
   def __str__(self):
      return "%s {%s} [%s]" % tuple(self)

class Condition(List):
   def __str__(self):
      return "%s | %s in {%s}" % tuple(self)

class Forbidden(List):
   def __str__(self):
      fmt = "{%s}" % ",".join(["%s=%s"]*(len(self)/2))
      return fmt % tuple(self)

class Parameters(List):
   def __str__(self):
      return "".join(["%s\n" % x for x in self])

class Domain(List):
   def __str__(self):
      return "%s" % ",".join(self)

class DomainFile(Domain):
   def __init__(self, f_name):
      domain = file(f_name).read().strip().split("\n")
      super(Domain,self).__init__(*domain)

class CefFile(Domain):
   def __init__(self, f_name):
      domain = file(f_name).read().strip().split("\n")
      super(Domain,self).__init__(*map(cef2block,domain))

DOMAIN = {
	"freq": "1,2,3,4,5,8,10,13,21,34",
   #"cefs": CefFile("cefs.txt"),
   #"prio": DomainFile("prios.txt"),
   "prio": "SimulateSOS,PreferGroundGoals,PreferUnitGroundGoals,DeferSOS,ByNegLitDist,ByCreationDate,PreferProcessed,PreferGoals,ConstPrio,PreferNonGoals",
   "level": "1,0,2", 
   "weight": "1,200,20,10,300,18,400,50,0,3,2,-1,4,7,-2,5,100,9999", 
   "cost":   "1,200,20,10,300,18,400,50,0,3,2,-1,4,7,-2,5,100,9999", 
   #"cost": "0,1,5,10,100,9999",
   "mult": "0.8,1,4,1.5,0.1,0.3,0.2,0.5,0.7,1,3,2,5,4,3,2,2.5,9999.9", 
   "factor": "1,1.5,2",
   "var": "0,1",
   "rel": "0,1,2,3",
   "ext": "0,1,2",
   "docs": "0,1",
   "fact": "0,1,10,9999.9",
   "real": "0,0.1,0.5,1,5,10,100,9999.9",
}


ARGS = Parameters(
   Arg("tord", "Auto,LPO4,KBO,KBO6", "LPO4"),
   Arg("sel", "SelectMaxLComplexAvoidPosPred,SelectNewComplexAHP,SelectComplexG,SelectCQPrecWNTNp", "SelectMaxLComplexAvoidPosPred"),
   Arg("prord", "arity,invfreq,invfreqconstmin", "invfreqconstmin"),
   Arg("simparamod", "none,normal,oriented", "normal"),
   Arg("srd", "0,1", "0"),
   Arg("forwardcntxtsr", "0,1", "1"),
   Arg("splaggr", "0,1", "1"),
   Arg("splcl", "0,4,7", "4"),
   Arg("sineL", "10,20,40,60,80,100,500,20000", "100"),
   Arg("sineR", "UU,01,02,03,04", "UU"),
   Arg("sinegf", "1.1,1.2,1.4,1.5,2.0,5.0,6.0", "1.2"),
   Arg("sineh ", "hypos,none", "hypos"),
   Arg("sine", "0,1", "0"),
)

CONDITIONS = Parameters(
   Condition("sineL",  "sine", "1"),
   Condition("sineR",  "sine", "1"),
   Condition("sinegf", "sine", "1"),
   Condition("sineh",  "sine", "1")
)

FORBIDDENS = Parameters()

WEIGHTS = {
   "ClauseWeightAge":                  "prio:prio f:weight v:weight pos:mult w:mult",
   "Clauseweight":                     "prio:prio f:weight v:weight pos:mult",
   "ConjectureGeneralSymbolWeight":    "prio:prio f:weight c:weight p:weight conj_f:weight conj_c:weight conj_p:weight v:weight maxt:mult maxl:mult pos:mult",
   "ConjectureRelativeSymbolWeight":   "prio:prio conj:mult f:weight c:weight p:weight v:weight maxt:mult maxl:mult pos:mult",
   "ConjectureSymbolWeight":           "prio:prio f:weight p:weight conj_f:weight conj_p:weight v:weight maxt:mult maxl:mult pos:mult",
   "Defaultweight":                    "prio:prio",
   "FIFOWeight":                       "prio:prio",
   "OrientLMaxWeight":                 "prio:prio f:weight v:weight unlit:mult maxl:mult pos:mult",
   "PNRefinedweight":                  "prio:prio f:weight v:weight nf:weight nv:weight maxt:mult maxl:mult pos:mult",
   "Refinedweight":                    "prio:prio f:weight v:weight maxt:mult maxl:mult pos:mult",
   "RelevanceLevelWeight":             "prio:prio const:level lin:level square:level default:level f:weight c:weight p:weight v:weight maxt:mult maxl:mult pos:mult",
   "RelevanceLevelWeight2":            "prio:prio const:level lin:level square:level default:level f:weight c:weight p:weight v:weight maxt:mult maxl:mult pos:mult",
   "StaggeredWeight":                  "prio:prio stagger:factor",
   "SymbolTypeweight":                 "prio:prio f:weight v:weight c:weight p:weight maxt:mult maxl:mult pos:mult",
   "Uniqweight":                       "prio:prio",
   "ConjectureRelativeTermWeight":     "prio:prio var:var rel:rel conj:mult f:weight c:weight p:weight v:weight ext:ext maxt:mult maxl:mult pos:mult",
   "ConjectureTermTfIdfWeight":        "prio:prio var:var rel:rel docs:docs tffact:fact ext:ext maxt:mult maxl:mult pos:mult",
   "ConjectureTermPrefixWeight":       "prio:prio var:var rel:rel match:real mis:real ext:ext maxt:mult maxl:mult pos:mult",
   "ConjectureLevDistanceWeight":      "prio:prio var:var rel:rel ins:cost del:cost ch:cost ext:ext maxt:mult maxl:mult pos:mult",
   "ConjectureTreeDistanceWeight":     "prio:prio var:var rel:rel ins:cost del:cost ch:cost ext:ext maxt:mult maxl:mult pos:mult",
   "ConjectureStrucDistanceWeight":    "prio:prio var:var rel:rel varmis:real symmis:real inst:real gen:real ext:ext maxt:mult maxl:mult pos:mult",
}

MIN_SLOTS = 3

def make_cef(weight, fparams, prefix=""):
   args = [x.split(":")[0] for x in WEIGHTS[weight].split(" ")]
   args = [fparams[prefix+x] for x in args]
   return "%s(%s)" % (weight, ",".join(args))

def params_update_finetunes(global_params, tunes_params):
   slots = int(global_params["slots"])
   ret = {}
   for i in range(slots):
      cef_key = "cef%d"%i
      cef_old = global_params[cef_key]
      weight = cef_old.split("__")[0]
      cef_new = make_cef(weight, tunes_params, prefix=cef_key+"_")
      cef_new = cef2block(cef_new)

      global_params[cef_key] = cef_new
      if cef_old != cef_new:
         ret[cef_old] = cef_new
   return ret
      
def cefs_args(slots, cefs):
   args = [Arg("slots",Domain(*[str(x) for x in range(MIN_SLOTS,slots+1)]),str(MIN_SLOTS))]
   for i in range(slots):
      args += [Arg("freq%d"%i, DOMAIN["freq"], "1")]
      args += [Arg("cef%d"%i, cefs, cefs[i])]
   return Parameters(*args)

def cefs_conditions(slots, cefs):
   conditions = []
   for i in range(MIN_SLOTS,slots):
       dom = ",".join(map(str,range(i+1,slots+1)))
       conditions += [Condition("freq%d"%i, "slots", dom)]
       conditions += [Condition("cef%d"%i, "slots", dom)]
   return Parameters(*conditions)

def cefs_forbiddens(slots, cefs):
   forbiddens = []
   for n in range(MIN_SLOTS,slots+1):
      forbiddens += ["#%d" % n]
      ns = range(0,n)
      pairs = [(i,j) for i in ns for j in ns if i<j]
      for cef in cefs:
         for (i,j) in pairs:
            forbiddens += [Forbidden("slots",n,"cef%d"%i,cef,"cef%d"%j,cef)]
   return Parameters(*forbiddens)

def parameters_global(slots, cefs):
   parts = ARGS + cefs_args(slots,cefs)+\
      CONDITIONS + cefs_conditions(slots,cefs)+\
      FORBIDDENS + cefs_forbiddens(slots,cefs)
   return Parameters(*parts)

def parameters_set_default(params, defaults):
   for param in params:
      if not isinstance(param, Arg):
         continue
      if param[0] in defaults:
         param[2] = defaults[param[0]]
      if param[2] not in param[1]:
         print "SHOULD NOT HAPPEN: Setting default for %s to %s" % (param[0], param[1][0])
         param[2] = param[1][0]


def parameters_finetune(cef, prefix=""):
   wargs = cef.replace("_M_","-").replace("_D_",".").split("__")
   weight = wargs.pop(0)
   args = []
   argtyps = [x.split(":") for x in WEIGHTS[weight].split(" ") if x]
   for (arg,typ) in argtyps:
      dom = DOMAIN[typ]
      #default = str(dom).split(",")[0] # yeah, ugly
      default = wargs.pop(0)
      args += [Arg(prefix+arg,dom,default)]
   return Parameters(*args)

def parameters_finetunes(params):
   slots = int(params["slots"])
   args = []
   for i in range(slots):
      args += ["#"+params["cef%d"%i]]
      args += parameters_finetune(params["cef%d"%i],"cef%d_"%i)
   return Parameters(*args)


SCENARIO_GLOBAL = """algo = %s
execdir = .
deterministic = 1
run_obj = runlength
overall_obj = mean
cutoff_time = %s
cutoff_length = max
tunerTimeout = %s
paramfile = %s/params.txt
outdir = %s/paramils-out
instance_file = %s
test_instance_file = data/empty.tst
"""

SCENARIO_FINETUNE = """algo = %s %s
execdir = .
deterministic = 1
run_obj = runlength
overall_obj = mean
cutoff_time = %s
cutoff_length = max
tunerTimeout = %s
paramfile = %s/params.txt
outdir = %s/paramils-out
instance_file = %s
test_instance_file = data/empty.tst
"""

SCENARIO_FINETUNES = """algo = %s %s
execdir = .
deterministic = 1
run_obj = runlength
overall_obj = mean
cutoff_time = %s
cutoff_length = max
tunerTimeout = %s
paramfile = %s/params.txt
outdir = %s/paramils-out
instance_file = %s
test_instance_file = data/empty.tst
"""

def scenario_global(cutoff, timeout, d_dir, instance_file, bin="epymils_globaltune.py"):
   return SCENARIO_GLOBAL % (bin, cutoff, timeout, d_dir, d_dir, instance_file)

def scenario_finetune(parstr, cutoff, timeout, d_dir, instance_file, bin="epymils_finetune.py"):
   return SCENARIO_FINETUNE % (bin, parstr, cutoff, timeout, d_dir, d_dir, instance_file)

def scenario_finetunes(parstr, cutoff, timeout, d_dir, instance_file, bin="epymils_finetunes.py"):
   return SCENARIO_FINETUNES % (bin, parstr, cutoff, timeout, d_dir, d_dir, instance_file)


E_PROTO_ARGS = "--definitional-cnf=24 %(splaggr)s %(splcl)s %(srd)s %(simparamod)s %(forwardcntxtsr)s --destructive-er-aggressive --destructive-er --prefer-initial-clauses -t%(tord)s %(prord)s -F1 --delete-bad-limit=150000000 -W%(sel)s %(sine)s %(heur)s"
      
E_SINE_ARGS = "--sine='GSinE(CountFormulas,%(sineh)s,%(sinegf)s,,%(sineR)s,%(sineL)s,1.0)'"

def e_update_arguments(params):
   eargs = dict(params)
   # default params
   eargs["splaggr"] = "--split-aggressive" if eargs["splaggr"] == "1" else ""
   eargs["srd"] = "--split-reuse-defs" if eargs["srd"] == "1" else ""
   eargs["forwardcntxtsr"] = "--forward-context-sr" if eargs["forwardcntxtsr"] == "1" else ""
   eargs["splcl"] = "--split-clauses="+eargs["splcl"] if eargs["splcl"]!="0" else ""
   if eargs["simparamod"] == "none":
      eargs["simparamod"] = ""
   elif eargs["simparamod"] == "oriented":
      eargs["simparamod"] = "--oriented-simul-paramod"
   else:
      eargs["simparamod"] = "--simul-paramod"
   if eargs["prord"] == "invfreq":
      eargs["prord"] = "-winvfreqrank -c1 -Ginvfreq"
   else:
      eargs["prord"] = "-G" + eargs["prord"]
   # SinE
   if eargs["sine"] == "1":
      eargs["sineh"] = "" if eargs["sineh"] == "none" else eargs["sineh"]
      eargs["sineR"] = "" if eargs["sineR"] == "UU" else eargs["sineR"]
      eargs["sine"] = E_SINE_ARGS % eargs
   else:
      eargs["sine"] = ""
   # heuristic
   slots = int(eargs["slots"])
   cefs = []
   for i in range(slots):
      cefs += ["%s*%s" % (eargs["freq%d"%i],block2cef(eargs["cef%d"%i]))]
   cefs.sort()
   eargs["heur"] = "-H'(%s)'" % ",".join(cefs)
   return eargs

def e_proto(params):
   eargs = e_update_arguments(params)
   return E_PROTO_ARGS % eargs

def e_arguments(params):
   eargs = e_update_arguments(params)
   return E_RUN_ARGS+(E_PROTO_ARGS % eargs)

def parameters_size(params):
   sizes = [arg[1].count(",")+1 for arg in params if type(arg) is Arg]
   return reduce(lambda x,y:x*y, sizes) if sizes else 0

#ps = parameters_global(6, DOMAIN["cefs"])
#print ps

def run_paramils(scenariofile, binary="./param_ils_2_3_run.rb", count=1, N="100", validN="800", init="1", out=None):
   def make_args(numRun):
      return [binary, "-numRun", numRun, "-scenariofile", scenariofile, "-N", N,"-validN", validN, "-init", init, "-output_level", "0", "-userunlog", "0"]
   if not out:
      out = open(os.devnull, 'w')
   args = [make_args(str(n)) for n in range(count)]
   ps = [subprocess.Popen(arg,stdout=out,close_fds=True,stderr=subprocess.STDOUT) for arg in args]
   #ps = [subprocess.Popen(arg) for arg in args]
   rets = [p.wait() for p in ps]
   if 1 in rets:
      sys.stdout.write("ERROR: Running paramils (return codes) %s\n" % str(rets))
   return rets

def clean_params(params):
   "Remove unused slots from params"
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

def best_params(outdir, report_quality=False, select_index=-1):
   fs = [f for f in os.listdir(outdir) if "traj" in f and f.endswith(".txt")]
   rs = [file(os.path.join(outdir,f)).readlines()[select_index].strip().split(",") for f in fs]
   if not rs:
      return None
   # the best ... the highest `ProblemCount` (r[2]) with the lowest `Quality` (r[1])
   best = min(rs, key=lambda r: (-int(r[2]),float(r[1])))
   if report_quality:
      print "BEST:\tT = %ss   Q =%s   # =%s" % (int(float(best[0])),best[1],best[2])
   params = [p.split("=") for p in best[5:]]
   params = {p[0].strip():p[1].strip("' ") for p in params}
   
   #clean_params(params)
   
   return params

