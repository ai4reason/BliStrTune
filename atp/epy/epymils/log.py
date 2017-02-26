import sys
from os.path import join
from .eargs import e_proto, E_SINE_ARGS
from .data import block2cef
from .. import eprover

def log(msg, args=None):
   if args:
      args = [str(x) for x in args]
   sys.stdout.write(msg+("\t"+("\n\t".join(args)) if args else "")+"\n")
   sys.stdout.flush()

def log_params(params, label):
   hash = eprover.protocol.proto_hash(e_proto(params))
   log("")
   log(label+"\t[ eproto/%s/%s/%s ]" % (hash[0:3], hash[3:6], hash))
   log("\t%(tord)s %(sel)s %(prord)s %(simparamod)s srd=%(srd)s forwardcntxtsr=%(forwardcntxtsr)s splaggr=%(splaggr)s splcl=%(splcl)s" % params)
   if params["sine"]=="1":
      log("\t"+(E_SINE_ARGS % params))
   log("", ["%s*%s" % (params["freq%d"%i],block2cef(params["cef%d"%i])) for i in range(int(params["slots"]))])

def log_proto(name, params):
   file(join("protos", name),"w").write(e_proto(params))


