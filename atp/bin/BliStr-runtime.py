#!/usr/bin/python

from os import listdir
from os.path import getmtime, join

end =  getmtime("nohup.out")
start = min([getmtime(join("prots",x)) for x in listdir("prots")])

days = int((end-start)/(24*3600))
hours = ((end-start)-(days*24*3600))/3600

print "%dd%dh" % (days,hours)

