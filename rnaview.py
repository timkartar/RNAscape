from Bio.PDB import MMCIFParser
import Bio
import json
import re, os, sys
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from get_helix_coords import get_helix_coords, process_resid
from plot import Plot
from math import cos, sin
from config import DSSR_PATH, CIF_PATH, FIG_PATH
import re 
from sklearn.neighbors import KDTree

dssrout = None
tree=None

def sorted_nicely( l ): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def circularLayout(n, m, d, theta, factor=False):
    poses = []
    rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
    for i in range(n):
        d = np.dot(rot, d)

        if factor:
            poses.append(m+d*np.sqrt(n))
        else:
            poses.append(m+d)

    return poses

def perp(v):
    v = v.tolist() + [0]
    z = [0,0,1]
    p = np.cross(v,z)[:2]
    p = p/(np.linalg.norm(p)+0.00000001)
    return p

def updateLoopPoints(start_pos, end_pos, val, helix_coords, factor=False):
    m = (start_pos + end_pos)/2
    poses = []
    v = (end_pos - start_pos)
    
    p = perp(v)
    ## generate points circularly using m,v,p
    n = len(val)
    d = start_pos - m
    
    
    theta = np.pi/(n+1)
    poses = circularLayout(n,m,d,theta, factor)
    neg_poses = circularLayout(n,m,d,-1*theta, factor)
    helix_coords_m = np.mean(helix_coords, axis=0)
    poses_m = np.mean(poses, axis=0)
    neg_poses_m = np.mean(neg_poses, axis=0)
    
    dis = np.linalg.norm(poses_m - helix_coords_m)
    n_dis = np.linalg.norm(neg_poses_m - helix_coords_m)
    
    if len(poses) == 0:
        return poses
    
    l = tree.query_radius(poses, r=5, count_only=True).sum()
    n_l = tree.query_radius(neg_poses, r=5, count_only=True).sum()
    
    if l < n_l:
        return poses
    else:
        return neg_poses

def generate_coords(helix_coords, helix_ids, dic, helix_dssrids, dssrout):
    pairs = []
    for item in dssrout['pairs']:
        pairs.append((item['nt1'],item['nt2']))

    
    positions = []
    markers = []
    ids = []
    chids = []
    dssrids = []
    for key, val in dic.items():
        start = key[0]
        end = key[1]
        if(start == None or end ==None):
            continue
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
            if pos in helix_coords:
                p = perp(v)
                tpos = pos + p*2 + v/(2*(l+1)) ## perpeindicular and out shift for overlap
                neg_tpos = pos - p*2 + v/(2*(l+1)) ## perpeindicular and out shift for overlap
                l = tree.query_radius([tpos], r=5, count_only=True)
                n_l = tree.query_radius([neg_tpos], r=5, count_only=True)
                #if dis > n_dis:
                if l < n_l:
                    pos = tpos
                else:
                    pos = neg_tpos

           
            t_poses.append(pos)
            t_chids.append(item[2])
            t_dssrids.append(item[3])
        v = helix_coords[start] - helix_coords[end]
        if (helix_dssrids[start], helix_dssrids[end]) in pairs or (helix_dssrids[end], helix_dssrids[start]) in pairs:
            t_poses = updateLoopPoints(start_pos, end_pos, val, helix_coords)
        elif np.linalg.norm(v) < 3: #threshold for bulging
            t_poses = updateLoopPoints(start_pos, end_pos, val, helix_coords, factor=True) 
        elif np.linalg.norm(v)/(len(val) +  0.0001) < 1.5: #threshold for bulging
            t_poses = updateLoopPoints(start_pos, end_pos, val, helix_coords, factor=True) 
        #else:
        #    t_poses = updateLoopPoints(start_pos, end_pos, val, helix_coords) 
        positions+=(t_poses)
        markers+=(t_markers)
        ids+=(t_ids)
        chids+=(t_chids)
        dssrids+=(t_dssrids)
    
    return positions, markers, ids, chids, dssrids

def get_linear_coords(nts, helix_ids, helix_coords, dssrids, dssrout):
    dic = {} #keys are like (start, end) values are like [(nt_id, rest1),...]

    start = None
    end = None
    l = []
    prev = False
    covered = []
    starters = []
    
    for item in dssrout['nts']:
        spl1, nt_id, rest1, chid =  process_resid(item['nt_id'])  

        if nt_id not in helix_ids or item['nt_id'] not in dssrids:
            starters.append((nt_id, rest1, chid, item['nt_id']))
        else:
            break

    enders = []
    for item in dssrout['nts'][::-1]:
        spl1, nt_id, rest1, chid =  process_resid(item['nt_id'])
        if nt_id not in helix_ids or item['nt_id'] not in dssrids:      
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
                start = dssrids.index(item['nt_id'])
                covered += l
                l = []

        else:
            prev = True
            l.append((nt_id, rest1, chid, item['nt_id'])) 
    
    return generate_coords(helix_coords, helix_ids, dic, dssrids, dssrout)        

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

def getTails(helix_dssrids, dssrids, chids, points):
    starters = {}
    enders = {}
    for item in np.unique(chids):
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
                starting=True
    
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
                ending=True
    #print(starters, enders)
    
    for k in starters.keys():
        if len(starters[k]) == 0:
            continue
        ip1 = starters[k][-1] + 1
        ip2 = starters[k][-1] + 2

        v = points[ip1] - points[ip2]
        n = len(starters[k])
        for i in range(len(starters[k])):
            #print(dssrids[ip1], dssrids[ip2], dssrids[starters[k][n-i-1]])
            points[starters[k][n-i-1]] = points[ip1] + v*(i+1)
            #print(points[ip1],points[ip2], points[starters[k][n-i-1]])

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


#if __name__ == "__main__":
def rnaView(prefix):
    global tree, dssrout
    #prefix = sys.argv[1]
    #if os.path.exists("{}/{}.png".format(FIG_PATH, prefix)):
    #    sys.exit()
    parser = MMCIFParser()
    #model = parser.get_structure(prefix,"./vn/{}-assembly1.cif".format(prefix))[0]
    model = parser.get_structure(prefix,"{}/{}-assembly1.cif".format(CIF_PATH, prefix))[0]
    
    
    with open("{}/{}-dssr.json".format(DSSR_PATH, prefix),"r") as f:
        dssrout = json.load(f)

    helices = get_helix_coords(dssrout, model)
    if helices == None:
        print("no helices in this structure")
        from PIL import Image, ImageFont

        text = "No helices in this structure"
        font_size = 36
        font_filepath = "/home/raktim/anaconda3/lib/python3.9/site-packages/matplotlib/mpl-data/fonts/ttf/Helvetica.ttf"
        color = (67, 33, 116)

        font = ImageFont.truetype(font_filepath, size=font_size)
        mask_image = font.getmask(text, "L")
        img = Image.new("RGBA", mask_image.size)
        img.im.paste(color, (0, 0) + mask_image.size, mask_image)  # need to use the inner `img.im.paste` due to `getmask` returning a core
        img.save('{}/{}.png'.format(FIG_PATH, prefix))


    else:
        helix_points, helix_ids, helix_markers, helix_chids, helix_dssrids = get_helix_coords(dssrout, model)
        tree=KDTree(helix_points)
        '''
        l = [helix_points, helix_ids, helix_markers, helix_chids, helix_dssrids]
        for item in l:
            print(len(item))

        for i in range(len(helix_markers)):
            plt.scatter(helix_points[i,0], helix_points[i,1], marker=helix_markers[i], edgecolors='none', color='black', s=200)
        plt.show()
        '''
        '''
        print(helix_dssrids,
                helix_points,
                helix_chids)
        '''
        
        rest_positions, rest_markers, rest_ids, rest_chids, rest_dssrids = get_linear_coords(dssrout,
                helix_ids, helix_points, helix_dssrids, dssrout)
        
        points = np.array(helix_points.tolist() + rest_positions)
        
        markers = helix_markers + rest_markers
        
        ids = helix_ids + rest_ids
        
        chids = helix_chids + rest_chids
        dssrids = helix_dssrids + rest_dssrids
        
        points, markers, ids, chids, dssrids, dic = orderData(points, markers, ids, chids, dssrids)
        #points = updateLoopPoints(points, dssrids, dssrout)
        
        idx = (np.argsort(chids, kind='mergesort'))
        chids = np.array(chids)[idx].tolist()

        ids = np.array(ids)[idx].tolist()

        markers = np.array(markers)[idx].tolist()

        dssrids = np.array(dssrids)[idx].tolist()
        points= points[idx,:]
        

        starters, enders, points = getTails(helix_dssrids, dssrids, chids, points)
        Plot(points, markers, ids, chids, dssrids, dssrout, prefix)
    return points, markers, ids, chids, dssrids, dssrout, prefix
