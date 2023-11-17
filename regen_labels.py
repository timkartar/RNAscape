from plot import Plot
import numpy as np
import json
from config import *
import sys


# grab the time string, and the rotation!
# everything else is chilling

time_string = sys.argv[1]
rotation = int(sys.argv[2])


npz_filepath = "{}/saved_output/{}.npz".format(MEDIA_PATH,time_string)
json_filepath = f"{MEDIA_PATH}/saved_output/{time_string}_dssrout.json"

# Code to open if necessary!
npzfile = np.load(npz_filepath)
points = npzfile['points']
markers = npzfile['markers']
ids = npzfile['ids']
chids = npzfile['chids']
prefix= npzfile['prefix']
dssrids = npzfile['dssrids']

bp_type = npzfile['bp_type']
time_string = npzfile['time_string']
out_path = str(npzfile['out_path'])


# Open and read the JSON file to get the object
with open(json_filepath, 'r') as json_file:
    dssrout = json.load(json_file)

figpath = Plot(points, markers, ids, chids, dssrids, dssrout, prefix, bp_type=bp_type, out_path=out_path, time_string=time_string, rotation=rotation)
print(figpath)