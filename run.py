from rnaview import rnaView
import os, sys, subprocess
from config import *
#from plot import Plot

cif = "/home/aricohen/Desktop/rnaview/backend/media/{}".format(sys.argv[1].strip())
prefix = sys.argv[2]
prefix = prefix.split('.cif')[0].strip()

# cif = "{}/{}-assembly1.cif".format(CIF_PATH, prefix)
json = "{}/{}-dssr.json".format(DSSR_PATH, prefix)
subprocess.run(["x3dna-dssr","-i={}".format(cif),"-o={}".format(json),"-idstr=long","--json"])
points, markers, ids, chids, dssrids, dssrout, prefix, figpath = rnaView(prefix, cif, json)
print(figpath.split('media')[1]) #NAME MEDIA CANNOT BE IN NAME CURRENTLY!
# can call Plot later again using this return
#Plot(points, markers, ids, chids, dssrids, dssrout, prefix)
