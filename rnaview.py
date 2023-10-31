from Bio.PDB import MMCIFParser
import Bio
import json
import re, os, sys
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from get_helix_coords import get_helix_coords, process_resid
from plot import Plot

import re 

def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def generate_coords(helix_coords, helix_ids, dic):
    positions = []
    markers = []
    ids = []
    chids = []
    dssrids = []

    for key, val in dic.items():
        start_pos = helix_coords[key[0]]
        end_pos = helix_coords[key[1]]
        t_poses = []
        t_markers = []
        t_ids = []
        t_chids = []
        t_dssrids = []

        l = len(val)
        for item in val:
            t_ids.append(item[0]) 
            t_markers.append("${}$".format(item[1]))
            v = (end_pos - start_pos)
            #v = v/np.linalg.norm(v)
            pos = start_pos + v*(val.index(item)+1)/(l+1)
            t_poses.append(pos)
            t_chids.append(item[2])
            t_dssrids.append(item[3])
        
        positions+=(t_poses)
        markers+=(t_markers)
        ids+=(t_ids)
        chids+=(t_chids)
        dssrids+=(t_dssrids)
    

    return positions, markers, ids, chids, dssrids

def get_linear_coords(nts, helix_ids, helix_coords):
    dic = {} #keys are like (start, end) values are like [(nt_id, rest1),...]

    start = None
    end = None
    l = []
    prev = False
    covered = []
    
    starters = []
    for item in dssrout['nts']:
        spl1, nt_id, rest1, chid =  process_resid(item['nt_id'])  

        if nt_id not in ids:
            starters.append((nt_id, rest1, chid, item['nt_id']))
        else:
            break

    enders = []
    for item in dssrout['nts'][::-1]:
        spl1, nt_id, rest1, chid =  process_resid(item['nt_id'])
        if nt_id not in ids:      
            enders.append((nt_id, rest1, chid, item['nt_id']))
        else:
            idx = ids.index(nt_id)
            break
    dic[(0,0)] = starters
    dic[(idx, idx)] = enders
    for item in dssrout['nts']:
        spl1, nt_id, rest1, chid =  process_resid(item['nt_id'])

        if nt_id in ids:
            if prev == False:
                start = ids.index(nt_id)
            else:
                end = ids.index(nt_id)
                prev = False
                dic[(start, end)] = l
                covered += l
                l = []

        else:
            prev = True
            l.append((nt_id, rest1, chid, item['nt_id'])) 
    
    return generate_coords(helix_coords, helix_ids, dic)        

if __name__ == "__main__":
    prefix = sys.argv[1]
    parser = MMCIFParser()
    model = parser.get_structure(prefix,"./vn/{}-assembly1.cif".format(prefix))[0]
    
    '''
    for item in model.get_residues():
        print(item.get_id())
    '''
    with open("./{}.json".format(prefix),"r") as f:
        dssrout = json.load(f)

    points, ids, markers, chids, dssrids = get_helix_coords(dssrout, model)
    
    rest_positions, rest_markers, rest_ids, rest_chids, rest_dssrids = get_linear_coords(dssrout, ids, points)
    
    points = np.array(points.tolist() + rest_positions)
    
    markers = markers + rest_markers
    
    ids = ids + rest_ids
    
    chids = chids + rest_chids
    dssrids = dssrids + rest_dssrids
    
    '''
    for i in range(len(markers)):
        plt.scatter(points[i,0], points[i,1], marker=markers[i], edgecolors='none', color='black',
                s=200
                )
    #plt.show()
    '''
    unique_chains = np.unique(chids)
    d = {}
    for item in unique_chains:
        d[item] = []

    for i in range(len(ids)):
        d[chids[i]].append(ids[i][1])
    
    sorted_nice = []
    for k in d.keys():
        d[k] = np.sort(d[k])
        d[k] = ["{}{}".format(i,k) for i in d[k]]
        sorted_nice += d[k]

    resnumbers = [] 
    for i in range(len(ids)):
        resnumbers.append("{}{}".format(ids[i][1], chids[i]))
    
    
    argsorted = []
    
    for item in sorted_nice:
        argsorted.append(resnumbers.index(item))
    
    points = points[argsorted,:]
    markers = np.array(markers)[argsorted].tolist()
    chids = np.array(chids)[argsorted].tolist()
    dssrids = np.array(dssrids)[argsorted].tolist()
    ids = np.array(ids)[argsorted].tolist()

    Plot(points, markers, ids, chids, dssrids, dssrout)
    

    


