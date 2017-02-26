from .data import Arg, Condition, Forbidden, Parameters

TIMEOUT_GLOBAL = 5 
TIMEOUT_FINETUNES = 5
CUTOFF = 1
MIN_SLOTS = 2
SLOTS = 5
CORES = 4

ITERS = 2
PROBLEMS = "200"
INSTANCE_FILE = "data/problems.txt"

USE_ENIGMA = True

DOMAIN = {
	"freq": "1,2,3,4,5,8,10,13,21,34", 
   #"cefs": CefFile("cefs.txt"),
   #"prio": DomainFile("prios.txt"),
   "prio": "SimulateSOS,PreferGroundGoals,PreferUnitGroundGoals,DeferSOS,ByNegLitDist,ByCreationDate,PreferProcessed,PreferGoals,ConstPrio,PreferNonGoals", # never remove ConstPrio for enigma
   "level": "1,0,2", 
   "weight": "1,200,20,10,300,18,400,50,0,3,2,-1,4,7,-2,5,100,9999", 
   "cost":   "1,200,20,10,300,18,400,50,0,3,2,-1,4,7,-2,5,100,9999", 
   #"cost": "0,1,5,10,100,9999",
   "mult": "0.8,1,4,1.5,0.1,0.3,0.2,0.5,0.7,1,3,2,5,4,3,2,2.5,9999.9", # never remove 0.2 for enigma
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



