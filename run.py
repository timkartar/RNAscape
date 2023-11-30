from rnaview import rnaView
import os, sys, subprocess
from config import *
from plot import Plot
import time
import random
import json
import numpy as np
import json

#python run.py uploads/1ivs-assembly1.cif 1ivs 1 dssr

cif = "{}/{}".format(MEDIA_PATH,sys.argv[1].strip())
prefix = sys.argv[2]
prefix = prefix.split('.cif')[0].strip() # MUST INCLUDE CIF or breaks, error handle later!
cond_bulging = bool(int(sys.argv[3]))
bp_type = sys.argv[4]

out_path = ""
if bp_type.strip() == "rnaview":
    out_path = "{}/{}".format(MEDIA_PATH,sys.argv[5].strip())

# cif = "{}/{}-assembly1.cif".format(CIF_PATH, prefix)
json_path = "{}/{}-dssr.json".format(DSSR_PATH, prefix)

subprocess.run([X3DNA_PATH,"-i={}".format(cif),"-o={}".format(json_path),"-idstr=long","--json"], cwd=CWD)
points, markers, ids, chids, dssrids, dssrout, prefix = rnaView(prefix, cif, json_path,
        cond_bulging=cond_bulging)


# If just generating for the first time, call time string
# Otherwise no!
time_string = str(int(time.time())) + str(random.randint(0,100))

# Save output of rnaView function to enable regeneration of labels!
npz_filepath = "{}/saved_output/{}.npz".format(MEDIA_PATH,time_string)
np.savez(npz_filepath, points=points, markers=markers, ids=ids, dssrids=dssrids,
         chids=chids, prefix=prefix, bp_type=sys.argv[4], time_string=time_string, out_path=out_path)
# Generate the file path for the JSON file
json_filepath = f"{MEDIA_PATH}/saved_output/{time_string}_dssrout.json"
# Serialize and save dssrout as a JSON file
with open(json_filepath, 'w') as json_file:
    json.dump(dssrout, json_file)
    
figpath,pngpath = Plot(points, markers, ids, chids, dssrids, dssrout, prefix, bp_type=sys.argv[4], out_path=out_path, time_string=time_string)
print(figpath +"," + time_string + "," + pngpath)
