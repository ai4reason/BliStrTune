
def strip_proto(s):
   return s[s.index("_")+1:]

def parse_output(out):
   nodes = {}
   edges = {}
   tops = {}
   curs = []
   names = {}

   for line in out:
      line = line.rstrip()
      if line.startswith("ITER"):
         it = int(line.split(" ")[1])
         curs = []
         counter = 0
         tops[it] = curs
      if line.startswith("atpstr_"):
         node = line.split(":")[0]
         curs.append(node)
         nodes[node] = (nodes[node] if node in nodes else [])+[it]
      if "==>" in line:
         parts = line.split(" ")
         orig = strip_proto(parts[0])
         new = strip_proto(parts[2])
         names[new] = "init-%s" % orig
      if line.startswith("Improving"):
         src = line.split(" ")[1]
      if line.startswith("NEWSTR"):
         dst = line.split(" ")[1]
         edges[(src,dst)] = it
         names[dst] = "iter-%s-%s" % (it,counter)
         counter += 1
         src = None

   return (names,nodes,edges,tops,curs)



