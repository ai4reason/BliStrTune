
class List(list):
   "List which can be created like List(1,2,3) instead of list([1,2,3])."
   def __init__(self, *args):
      super(List,self).__init__(args)

class Arg(List):
   "Format ParamILS parameter in format 'arg {values} [default]'."
   def __str__(self):
      return "%s {%s} [%s]" % tuple(self)

class Condition(List):
   "Format ParamILS condition in format 'arg1 | arg2 in {values}'"
   def __str__(self):
      return "%s | %s in {%s}" % tuple(self)

class Forbidden(List):
   "Format ParamILS forbidden values in format '{arg1=val1,...}'."
   def __str__(self):
      fmt = "{%s}" % ",".join(["%s=%s"]*(len(self)/2))
      return fmt % tuple(self)

class Parameters(List):
   "Format ParamILS parameters, one on each line (using their str)."
   def __str__(self):
      return "".join(["%s\n" % x for x in self])

class Domain(List):
   "Format domain (comma separated values)."
   def __str__(self):
      return "%s" % ",".join(self)

class DomainFile(Domain):
   "Load domain values from file (one value a line)." 
   def __init__(self, f_name):
      domain = file(f_name).read().strip().split("\n")
      super(Domain,self).__init__(*domain)

class CefFile(Domain):
   "Load CEFs file (one CEF a line) and apply cef2block."
   def __init__(self, f_name):
      domain = file(f_name).read().strip().split("\n")
      super(Domain,self).__init__(*map(cef2block,domain))

def cef2block(cef):
   "Encode a CEF as a ParamILS string containg only [a-zA-Z0-9_]."
   return cef.replace("-","_M_").replace(",","__").replace(".","_D_").replace("(","__").replace(")","")

def block2cef(block):
    "Decode a CEF from a ParamILS string."
    parts = block.replace("_M_","-").replace("_D_",".").split("__")
    return "%s(%s)" % (parts[0],  ",".join(parts[1:]))

