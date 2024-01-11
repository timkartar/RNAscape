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
npzfile = np.load(npz_filepath, allow_pickle=True)
points = npzfile['points']
markers = npzfile['markers']
ids = npzfile['ids']
chids = npzfile['chids']
prefix= npzfile['prefix']
dssrids = npzfile['dssrids']

# bp_type = npzfile['bp_type'] # get from sysout
bp_type = sys.argv[3]
time_string = npzfile['time_string']
out_path = str(npzfile['out_path'])
# extra = json.loads(str(npzfile['extra']).replace("\'","\""))
extra_string = sys.argv[4]
extra_list = extra_string.split(',')
extra={'arrowsize':float(extra_list[2]), 'circlesize':float(extra_list[0]),
            'circle_labelsize':float(extra_list[1]), 'cols':[extra_list[3], extra_list[4],
                extra_list[5], extra_list[6], extra_list[7]],  #A,C,G,U,X
            'showNumberLabels':extra_list[8], 'numberSeparation': extra_list[9], 'numberSize': extra_list[10],
            'counter': extra_list[11],
}

# Open and read the JSON file to get the object
with open(json_filepath, 'r') as json_file:
    dssrout = json.load(json_file)

figpath, pngpath, log = Plot(points, markers, ids, chids, dssrids, dssrout, prefix, bp_type=bp_type, out_path=out_path, extra=extra,time_string=time_string, rotation=rotation)
print(figpath +",,," + pngpath)
