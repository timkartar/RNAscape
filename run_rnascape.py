import sys

# example: python run_rnascape.py 1ivs.cif 1ivs

# This file runs RNAscape on a cif or pdb file using your specified settings
# If downloading from the PDB, use the biological assembly file

# BEGIN USER SETTINGS ----------------------------------------------
# file must be cif or pdb
cif = sys.argv[1].strip()
prefix = sys.argv[2].strip()
X3DNA_PATH = '/home/aricohen/Desktop/DeepPBS/dependencies/bin/x3dna-dssr' # path to DSSR binary
json_path = './json/' # by default, DSSR output will be saved to the json folder
MEDIA_PATH = './output/' # where all output of RNAscape will be stored
FIG_PATH = '/processed_images/' # figures will be in MEDIA_PATH/FIG_PATH

# default arguments for RNAscape
cond_bulging = False # this bulges out all loops to create more space on the graph. Change to True to only conditionally bulge loops (condense them)
bp_type = "dssrLw" #BP annotation types: dssr, saenger, none
rotation = 0 # float between 0 and 360
extra={'arrowsize':1, 'circlesize':1,
            'circle_labelsize':1, 'cols':['#FF9896', '#AEC7E8', '#90CC84', '#DBDB8D', '#FFFFFF'], #A,C,G,U,X (non-standard)
            'showNumberLabels': False, 'numberSeparation': 1, 'numberSize': 1, 'counter': 0, 'markerSize': 1,
            'numberColor': 'saddlebrown', 
} # other small visual settings
# END USER SETTINGS -------------------------------------------------

from rnascape import rnascape
import os, sys, subprocess
from plot import Plot
import time
import random
import json
import numpy as np
import json

# run DSSR and save output to json folder
subprocess.run([X3DNA_PATH,"-i={}".format(cif),"-o={}/{}-dssr.json".format(json_path, prefix),"-idstr=long","--json","--prefix={}".format(prefix)], cwd=os.getcwd())
# -O of this is the problem!

points, markers, ids, chids, dssrids, dssrout, prefix = rnascape(prefix, cif, '{}/{}-dssr.json'.format(json_path, prefix),
        cond_bulging=cond_bulging)

# to keep track of each file
time_string = str(int(time.time())) + str(random.randint(0,100))

# keep track of important DSSR info
# json_filepath = f"{MEDIA_PATH}/saved_output/{time_string}_dssrout.json"
#with open(json_filepath, 'w') as json_file:
#    json.dump(dssrout, json_file)

figpath, pngpath, log = Plot(points, markers, ids, chids, dssrids, dssrout, prefix, 
                             bp_type=bp_type, extra=extra, time_string=time_string, 
                             rotation=rotation, FIG_PATH=FIG_PATH, MEDIA_PATH=MEDIA_PATH)

# Save output of RNAscape function to enable regeneration of labels!
# npz_filepath = "{}/saved_output/{}.npz".format(MEDIA_PATH,time_string)

with open("{}/saved_output/{}.log".format(MEDIA_PATH,time_string), 'w') as log_file:
    log_file.write(log)

# np.savez(npz_filepath, points=points, markers=markers, ids=ids, dssrids=dssrids,
#         chids=chids, prefix=prefix, bp_type=bp_type, extra=extra,
#         time_string=time_string, log=log)

# print non-WC nucleotides if applicable
print(log)