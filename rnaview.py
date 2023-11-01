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
        
        for i in range(len(val)):
            item = val[i]
            t_ids.append(item[0]) 
            t_markers.append("${}$".format(item[1]))
            v = (end_pos - start_pos)
            pos = start_pos + v*(i+1)/(l+1)

            t_poses.append(pos)
            t_chids.append(item[2])
            t_dssrids.append(item[3])
        positions+=(t_poses)
        markers+=(t_markers)
        ids+=(t_ids)
        chids+=(t_chids)
        dssrids+=(t_dssrids)
    
    return positions, markers, ids, chids, dssrids

def get_linear_coords(nts, helix_ids, helix_coords, dssrids):
    dic = {} #keys are like (start, end) values are like [(nt_id, rest1),...]

    start = None
    end = None
    l = []
    prev = False
    covered = []
    starters = []
    
    for item in dssrout['nts']:
        spl1, nt_id, rest1, chid =  process_resid(item['nt_id'])  

        if nt_id not in helix_ids and item['nt_id'] not in dssrids:
            starters.append((nt_id, rest1, chid, item['nt_id']))
        else:
            break

    enders = []
    for item in dssrout['nts'][::-1]:
        spl1, nt_id, rest1, chid =  process_resid(item['nt_id'])
        if nt_id not in helix_ids and item['nt_id'] not in dssrids:      
            enders.append((nt_id, rest1, chid, item['nt_id']))
        else:
            idx = dssrids.index(item['nt_id'])
            break
    
    dic[(0,0)] = starters
    dic[(idx, idx)] = enders
    
    curr_chain = None
    for item in dssrout['nts']:
        spl1, nt_id, rest1, chid =  process_resid(item['nt_id'])

        if nt_id in helix_ids and item['nt_id'] in dssrids:
            if prev == False:
                start = dssrids.index(item['nt_id'])
            else:
                end = dssrids.index(item['nt_id'])
                prev = False
                dic[(start, end)] = l
                covered += l
                l = []

        else:
            prev = True
            l.append((nt_id, rest1, chid, item['nt_id'])) 
    
    return generate_coords(helix_coords, helix_ids, dic)        

def orderData(points, markers, ids, chids, dssrids):
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
    
    done_indices = []
    for item in sorted_nice:
        idx = resnumbers.index(item)
        while idx in done_indices:
            idx+=1
        done_indices.append(idx)
        argsorted.append(idx)

    points = points[argsorted,:]
    markers = np.array(markers)[argsorted].tolist()
    chids = np.array(chids)[argsorted].tolist()
    dssrids = np.array(dssrids)[argsorted].tolist()
    ids = np.array(ids)[argsorted].tolist()
    
    return points, markers, ids, chids, dssrids, d

def getTails(dssrids, chids, points):
    starters = {}
    enders = {}
    for item in dic.keys():
        starters[item] = []
        enders[item] = []
    
    starting = True
    for i in range(len(dssrids)-1):
        chid = chids[i]
        if dssrids[i] not in helix_dssrids:
            if(starting):
                starters[chid].append(i)
        else:
            starting = False
            if chids[i+1] != chid:
                #starters[chid].append(i+1)
                starting=True
    
    #print(dssrids)
    ending = True
    for i in range(len(dssrids)-1):
        rev_dssrids = dssrids[::-1]
        rev_chids = chids[::-1]
        chid = rev_chids[i]
        
        if rev_dssrids[i] not in helix_dssrids:
            if(ending):
                enders[chid].append(len(dssrids) -1 - i)
        else:
            ending = False
            if rev_chids[i+1] != chid:
                #enders[chid].append(i+1)
                ending=True
    
    for k in starters.keys():
        if len(starters[k]) == 0:
            continue
        ip1 = starters[k][0] - 1
        ip2 = starters[k][0] - 2

        v = points[ip1] - points[ip2]
        for i in range(len(starters[k])):
            points[starters[k][i]] = points[ip1] + v*(i+1)
        

    for k in enders.keys():
        if len(enders[k]) == 0:
            continue
        enders[k] = enders[k][::-1]
        ip1 = enders[k][0] - 1
        ip2 = enders[k][0] - 2

        v = points[ip1] - points[ip2]
        for i in range(len(enders[k])):
            points[enders[k][i]] = points[ip1] + v*(i+1)
        

    return starters, enders, points


if __name__ == "__main__":
    prefix = sys.argv[1]
    parser = MMCIFParser()
    model = parser.get_structure(prefix,"./vn/{}-assembly1.cif".format(prefix))[0]
    
    
    with open("./{}.json".format(prefix),"r") as f:
        dssrout = json.load(f)

    helix_points, helix_ids, helix_markers, helix_chids, helix_dssrids = get_helix_coords(dssrout, model)
    
    rest_positions, rest_markers, rest_ids, rest_chids, rest_dssrids = get_linear_coords(dssrout,
            helix_ids, helix_points, helix_dssrids)
    
    points = np.array(helix_points.tolist() + rest_positions)
    
    markers = helix_markers + rest_markers
    
    ids = helix_ids + rest_ids
    
    chids = helix_chids + rest_chids
    dssrids = helix_dssrids + rest_dssrids
    
    '''
    for i in range(len(markers)):
        plt.scatter(points[i,0], points[i,1], marker=markers[i], edgecolors='none', color='black',
                s=200
                )
    #plt.show()
    '''

    points, markers, ids, chids, dssrids, dic = orderData(points, markers, ids, chids, dssrids)
    
    starters, enders, points = getTails(dssrids, chids, points)
    Plot(points, markers, ids, chids, dssrids, dssrout, prefix)
    

    


