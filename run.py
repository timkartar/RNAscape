from rnaview import rnaView
import os, sys, subprocess
from config import *
#from plot import Plot

prefix = sys.argv[1]
cif = "{}/{}-assembly1.cif".format(CIF_PATH, prefix)
json = "{}/{}-dssr.json".format(DSSR_PATH, prefix)
subprocess.run(["x3dna-dssr","-i={}".format(cif),"-o={}".format(json),"-idstr=long","--json"])

points, markers, ids, chids, dssrids, dssrout, prefix = rnaView(prefix)

# can call Plot later again using this return
#Plot(points, markers, ids, chids, dssrids, dssrout, prefix)
