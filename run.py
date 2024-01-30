from rnascape import rnascape
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
# rnascape file is 5,
extra={'arrowsize':1, 'circlesize':1,
            'circle_labelsize':1, 'cols':['#FF9896', '#AEC7E8', '#90CC84', '#DBDB8D', '#FFFFFF'], #A,C,G,U,X
            'showNumberLabels': True, 'numberSeparation': 1, 'numberSize': 1, 'counter': 0, 'markerSize': 1
            } 
if len(sys.argv) != 5: # append extra if length equals 5 (did not pass extra)
    extra_string = sys.argv[5]
    extra_list = extra_string.split(',')
    extra={'arrowsize':float(extra_list[2]), 'circlesize':float(extra_list[0]),
                'circle_labelsize':float(extra_list[1]), 'cols':[extra_list[3], extra_list[4],
                    extra_list[5], extra_list[6], extra_list[7]],  #A,C,G,U,X
                'showNumberLabels':extra_list[8], 'numberSeparation': extra_list[9], 'numberSize': extra_list[10],
                'counter': extra_list[11], 'markerSize': extra_list[12]
                }

# cif = "{}/{}-assembly1.cif".format(CIF_PATH, prefix)
json_path = "{}/{}-dssr.json".format(DSSR_PATH, prefix)

subprocess.run([X3DNA_PATH,"-i={}".format(cif),"-o={}".format(json_path),"-idstr=long","--json","--prefix={}".format(cif)], cwd=CWD)
subprocess.run([X3DNA_PATH,"-i={}".format(cif),"-o={}".format(json_path),"-idstr=long","--json","--prefix={}".format(cif),
    "--cleanup"], cwd=CWD)
points, markers, ids, chids, dssrids, dssrout, prefix = rnascape(prefix, cif, json_path,
        cond_bulging=cond_bulging)

# delete structure file
os.remove(cif)

time_string = str(int(time.time())) + str(random.randint(0,100))

# Generate the file path for the JSON file
json_filepath = f"{MEDIA_PATH}/saved_output/{time_string}_dssrout.json"

# Serialize and save dssrout as a JSON file
with open(json_filepath, 'w') as json_file:
    json.dump(dssrout, json_file)

figpath, pngpath, log = Plot(points, markers, ids, chids, dssrids, dssrout, prefix, bp_type=bp_type, extra=extra, out_path=out_path, time_string=time_string)
print(figpath +",,," + time_string + ",,," + pngpath)

# Save output of rnascape function to enable regeneration of labels!
npz_filepath = "{}/saved_output/{}.npz".format(MEDIA_PATH,time_string)

with open("{}/saved_output/{}.log".format(MEDIA_PATH,time_string), 'w') as log_file:
    log_file.write(log)

np.savez(npz_filepath, points=points, markers=markers, ids=ids, dssrids=dssrids,
         chids=chids, prefix=prefix, bp_type=bp_type, extra=extra,
         time_string=time_string, log=log)
