from os import getenv, system
from os.path import join, dirname, isdir

def mkdir(f_name):
   dir = dirname(f_name)
   if not isdir(dir):
      system("mkdir -p %s" % dir)

ATP_ROOT = getenv("ATP_ROOT", join(getenv("HOME"), "atp"))

import eprover
import epymils

__all__ = ["eprover", "epymils", "ATP_ROOT"]

