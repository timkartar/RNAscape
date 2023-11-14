from rnaview import rnaView
import os, sys, subprocess
from config import *
from plot import Plot

cif = "{}/{}".format(MEDIA_PATH,sys.argv[1].strip())
prefix = sys.argv[2]
prefix = prefix.split('.cif')[0].strip() # MUST INCLUDE CIF or breaks, error handle later!
cond_bulging = bool(int(sys.argv[3]))
bp_type = sys.argv[4]

# cif = "{}/{}-assembly1.cif".format(CIF_PATH, prefix)
json = "{}/{}-dssr.json".format(DSSR_PATH, prefix)
subprocess.run(["x3dna-dssr","-i={}".format(cif),"-o={}".format(json),"-idstr=long","--json"])
points, markers, ids, chids, dssrids, dssrout, prefix = rnaView(prefix, cif, json,
        cond_bulging=cond_bulging)
# can call Plot later again using this return
figpath = Plot(points, markers, ids, chids, dssrids, dssrout, prefix, bp_type=sys.argv[4])
print(figpath)
