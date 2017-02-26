import sys
from os import getenv, system
from os.path import join, dirname, isdir

def mkdir(f_name):
   dir = dirname(f_name)
   if not isdir(dir):
      system("mkdir -p %s" % dir)

def failed(msg):
   msg = msg.rstrip("\n")+"\n"
   sys.stderr.write(msg)
   try:
      file("failed.log","a").write(msg)
   except Exception:
      pass

ATP_ROOT = getenv("ATP_ROOT", join(getenv("HOME"), "atp"))

import eprover
import epymils

__all__ = ["eprover", "epymils", "ATP_ROOT"]

