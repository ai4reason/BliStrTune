from .data import block2cef

E_PROTO_ARGS = "--definitional-cnf=24 %(splaggr)s %(splcl)s %(srd)s %(simparamod)s %(forwardcntxtsr)s --destructive-er-aggressive --destructive-er --prefer-initial-clauses -t%(tord)s %(prord)s -F1 --delete-bad-limit=150000000 -W%(sel)s %(sine)s %(heur)s"
      
E_SINE_ARGS = "--sine='GSinE(CountFormulas,%(sineh)s,%(sinegf)s,,%(sineR)s,%(sineL)s,1.0)'"

def e_update_arguments(params):
   "Convert ParamILS params in format {key:val} to E arguments for formating E_PROTO_ARGS."

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

