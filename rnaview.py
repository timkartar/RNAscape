from Bio.PDB import MMCIFParser
import Bio
import json
import re, os, sys
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from get_helix_coords import get_helix_coords, process_resid

def generate_coords(helix_coords, helix_ids, dic):
    positions = []
    markers = []
    ids = []

    for key, val in dic.items():
        start_pos = helix_coords[key[0]]
        end_pos = helix_coords[key[1]]
        t_poses = []
        t_markers = []
        t_ids = []

        l = len(val)
        for item in val:
            t_ids.append(item[0]) 
            t_markers.append("${}$".format(item[1]))
            v = (end_pos - start_pos)
            #v = v/np.linalg.norm(v)
            pos = start_pos + v*(val.index(item)+1)/(l+1)
            t_poses.append(pos)
        
        positions+=(t_poses)
        markers+=(t_markers)
        ids+=(t_ids)
    

    return positions, markers, ids

def get_linear_coords(nts, helix_ids, helix_coords):
    dic = {} #keys are like (start, end) values are like [(nt_id, rest1),...]

    start = None
    end = None
    l = []
    prev = False
    covered = []
    
    starters = []
    for item in dssrout['nts']:
        spl1, nt_id, rest1 =  process_resid(item['nt_id'])  

        if nt_id not in ids:
            starters.append((nt_id, rest1))
        else:
            break

    enders = []
    for item in dssrout['nts'][::-1]:
        spl1, nt_id, rest1 =  process_resid(item['nt_id'])
        if nt_id not in ids:      
            enders.append((nt_id, rest1))
        else:
            idx = ids.index(nt_id)
            break
    print(starters, enders)
    dic[(0,0)] = starters
    dic[(idx, idx)] = enders
    for item in dssrout['nts']:
        spl1, nt_id, rest1 =  process_resid(item['nt_id'])

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
            l.append((nt_id, rest1)) 
    '''
    l=[]
    c = 0

    for item in dssrout['nts']:
        
        spl1, nt_id, rest1 =  process_resid(item['nt_id'])
        if (nt_id, rest1) in covered or nt_id in ids:
            c += 1
            continue
        else:
            l.append((nt_id, rest1))
    
    dic[(0, len('nts')-1)] = l ## fix dangling edges/loop TODO
    '''
    print(dic)
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

    points, ids, markers = get_helix_coords(dssrout, model)

    rest_positions, rest_markers, rest_ids = get_linear_coords(dssrout, ids, points)
    
    points = np.array(points.tolist() + rest_positions)
    markers = markers + rest_markers

    for i in range(len(markers)):
        plt.scatter(points[i,0], points[i,1], marker=markers[i], edgecolors='none', color='black',
                s=200
                )
    plt.show()
    

    


