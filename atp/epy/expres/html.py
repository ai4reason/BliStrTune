from os import getenv
from os.path import join
import json

from .. import mkdir

HTML_DIR = join(getenv("HOME"), "public_html", "expres")

HTML_TABLE = """<html>
<head>
   <title>%(prefix)s @ %(bid)s @ %(limit)ss</title>
   <link rel="stylesheet" type="text/css" href="static/style.css">
   <script src="static/sortable.js"></script>
   <script src="data/%(prefix)s_%(bid)s_%(limit)ss.js"></script>
   <script>
   window.onload = function() {
      updateTable(%(prefix)s_%(bid)s_%(limit)ss, "%(prefix)s_%(bid)s_%(limit)ss", %(index)d, -1);
   };
   </script>
</head>
<body>
<h1>Summary :: %(prefix)s @ %(bid)s @ %(limit)ss</h1>
<div class="tables">
<div class="box">
   <table id="%(prefix)s_%(bid)s_%(limit)ss"></table>
</div>
</div>
</body>
</html>
"""

def create_summary_data(prefix, bid, limit, summary, dir=HTML_DIR, usehash=False, usesotacs=True):
   bid = bid.replace("-","_")
   t = summary.table(usehash, usesotacs)

   f_js = join(dir,"data","%s_%s_%ss.js"%(prefix,bid,limit))
   mkdir(f_js)
   file(f_js,"w").write("var %s_%s_%ss = %s;" % (prefix,bid,limit,json.dumps(t)))

def create_summary(prefix, bid, limit, summary, dir=HTML_DIR, usehash=False, usesotacs=True):
   create_summary_data(prefix, bid, limit, summary, dir, usehash, usesotacs)

   f_html = join(dir,"%s-%s-%ss.html"%(prefix,bid,limit))
   mkdir(f_html)
   file(f_html,"w").write(HTML_TABLE % {
      "prefix": prefix,
      "bid": bid.replace("-","_"),
      "limit": limit,
      "index": 2 if usehash else 1
   })

