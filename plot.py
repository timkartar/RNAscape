import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import sre_yield
from config import FIG_PATH, MEDIA_PATH
from copy import deepcopy
from math import cos, sin
from get_helix_coords import process_resid
import time
import random
from read_rnaview import readRnaview
import os, sys
from config import *

plt.gca().invert_yaxis()
plt.gca().invert_xaxis()
style_dict = {}
arrow_dict = {}


chem_components = dict(np.load(CWD + "/modified_parents.npz",allow_pickle=True))
#python /home/aricohen/Desktop/rnaview/run.py uploads/7vnv-assembly1.cif 7vnv 1 rnaview uploads/7vnv-assembly1.cif.out

"""
Get index of a nucleotide from chain id and resid
"""
def getIndex(target_chid, target_resid, ids, chids):
    matching_ids_with_indices = [(index, sublist) for index, sublist in enumerate(ids) if str(sublist[1]) == str(target_resid)]
    for tuple in matching_ids_with_indices:
        cur_index = tuple[0]
        if chids[cur_index] == target_chid:
            return cur_index

"""
Use DSSR to get LW annotations rather than Rnaview file upload
"""
def getCustomMarker(pos, item):
    marker = item[1][pos]
    m = item[0][0]
    
    if pos == 0 :
        t = item[0][1]
    else:
        t = item[0][2]
    
    d = t - m
    d = d/np.linalg.norm(d)
    v = [0,1]
    angle = np.rad2deg(np.arccos(np.dot(d,v)))
    tanangle = np.rad2deg(np.arctan(d[1]/d[0]))

    if marker == ">":
        #print(angle, tanangle, item[1])

        if tanangle < 0 and angle <= 90:
            return (3,0, angle)
        if tanangle < 0 and angle > 90:
            return (3,0, -1*angle)
        
        if tanangle >= 0 and angle > 90:
            return (3,0, angle)
        if tanangle >= 0 and angle <= 90:
            return (3,0, -1*angle)
    
    if marker == "s":
        if tanangle < 0 and angle <= 90:
            return (4,0, angle + 45)
        if tanangle < 0 and angle > 90:
            return (4,0, -1*angle + 45)
        
        if tanangle >= 0 and angle > 90:
            return (4,0, angle + 45)
        if tanangle >= 0 and angle <= 90:
            return (4,0, -1*angle + 45)
    else:
        return marker

def getBasePairingEdgesDssrLw(dssrout, dssrids, points):
    dssr_lw_bp_types = list(sre_yield.AllStrings('[WHS][WHS]'))
    dssr_lw_bp_types.remove("WW")
    # ['HW', 'SW', 'WH', 'HH', 'SH', 'WS', 'HS', 'SS']
    #dssr_lw_markers = ['so', '<o', 'os', 'ss', '<s', 'o>', 's>', '<>']
    dssr_lw_markers = ['so', '>o', 'os', 'ss', '>s', 'o>', 's>', '>>']
    bp_map = {}
    for item in dssr_lw_bp_types:
        bp_map[item] = dssr_lw_markers[dssr_lw_bp_types.index(item)]
    magnification = max(1, min(len(dssrids)/40, 10))
    edges = []
    bp_markers = []

    for item in dssrout['pairs']:
        i1 = dssrids.index(item['nt1'])
        i2 = dssrids.index(item['nt2'])
        edges.append((i1, i2))
        style_dict[(i1, i2)] = ':'#'dashed'
        arrow_dict[(i1, i2)] = 0.001*magnification

        v = points[i1] - points[i2]
        d = np.linalg.norm(v)

        if d < 2: ## do not show bp type for too small edges
            continue
        p = points[i2]+v/2 
        typ = item['LW'][1]+ item['LW'][2]
        

        # Compute points for each shape based on directional vector
        direc = v / d
        SCALAR = 0.8
        p2 = p + (-1 * direc * SCALAR)
        p1 = p + (direc * SCALAR)
        p=[p,p1,p2] # use p if hoog/hoog or sugar/sugar, otherwise p1 and p2


        if "." in typ: # DSSR couldn't determine properly
            continue
        if typ == "WW": #do not show watson crick pairs
            continue
        if item['LW'][0] == 'c':
            orient = 'k'
        else:
            orient = 'w'
        bp_markers.append([p, bp_map[typ], orient, item['LW'][0]+typ])
    return edges, bp_markers, bp_map

def getBasePairingEdgesRnaview(points, ids, chids, out_path):
    rnaview_bp_types= ["{}/{}".format(e[0], e[1]) for e in list(sre_yield.AllStrings('[WHS][WHS]'))]
    rnaview_bp_types.remove("W/W")


    #rnaview_markers = ['so', '<o', 'os', 'ss', '<s', 'o>', 's>', '<>']
    rnaview_markers = ['so', '>o', 'os', 'ss', '>s', 'o>', 's>', '>>']
    
    bp_map = {}
    for item in rnaview_bp_types:
        bp_map[item] = rnaview_markers[rnaview_bp_types.index(item)]
    # ['H/W', 'S/W', 'W/H', 'H/H', 'S/H', 'W/S', 'H/S', 'S/S']
    
    magnification = max(1, min(len(points)/40, 10))
    edges = []
    bp_markers = []

    # GET OUTPUT FROM RNAView
    bp_list = readRnaview(out_path)

    for item in bp_list:
        chain_id = item["ch_id"]
        res_id = item["res_id"]
        i1 = int(getIndex(chain_id, res_id, ids, chids))
        
        chain_id2 = item["ch_id2"]
        res_id2 = item["res_id2"]
        i2 = int(getIndex(chain_id2, res_id2, ids, chids))

        edges.append((i1, i2))
        
        style_dict[(i1, i2)] = ':'#'dashed'
        arrow_dict[(i1, i2)] = 0.001*magnification
        v = points[i1] - points[i2]
        d = np.linalg.norm(v)

        if d < 2: ## do not show bp type for too small edges
            continue

        p = points[i2]+v/2

        # Compute points for each shape based on directional vector
        direc = v / d
        SCALAR = 0.8
        p2 = p + (-1 * direc * SCALAR)
        p1 = p + (direc * SCALAR)
        p=[p,p1,p2] # use p if hoog/hoog or sugar/sugar, otherwise p1 and p2

        typ = item["bp_type"]
        
        if "." in typ or "?" in typ: # RNAView couldn't determine properly
            continue
        if typ == "+/+" or typ == "-/-" or typ == "W/W": #do not show watson crick pairs
            continue
        if item['orient'].strip() == 'cis':
            orient = 'k'
        else:
            orient = 'w'
        bp_markers.append([p, bp_map[typ], orient, item['orient'][0]+typ]) # FOR NOW PASS IT LIKE HE HAS IT!

    return edges, bp_markers, bp_map
        
        # Get index of second nucleotide

    #     i1 = dssrids.index(item['nt1'])
    #     i2 = dssrids.index(item['nt2'])
    #     edges.append((i1, i2))
    #     style_dict[(i1, i2)] = ':'#'dashed'
    #     arrow_dict[(i1, i2)] = 0.001*magnification

    #     v = points[i1] - points[i2]
    #     d = np.linalg.norm(v)

    #     if d < 2: ## do not show bp type for too small edges
    #         continue
    #     p = points[i2]+v/2 
    #     typ = item['DSSR'][1]+ item['DSSR'][3]
        
    #     if "." in typ: # DSSR couldn't determine properly
    #         continue
    #     if typ == "WW": #do not show watson crick pairs
    #         continue
    #     if item['DSSR'][0] == 'c':
    #         orient = 'k'
    #     else:
    #         orient = 'w'
    #     bp_markers.append([p, bp_map[typ], orient, item['DSSR'][0]+typ])


def getBasePairingEdgesSaenger(dssrout, dssrids, points):
    #bp types: DSSR [ct][MWm][+-][MWm]
    dssr_bp_types = list(sre_yield.AllStrings('[012][0-9]'))
    l = [int(i) for i in dssr_bp_types]
    idx = np.argsort(l)
    dssr_bp_types = np.array(dssr_bp_types)[idx].tolist()
    # print(dssr_bp_types)
    
    #dssr_bp_types.remove("WW")
    
    #bp_marker_types = '[o^pdshP*]'
    #marker_bp_types = list(sre_yield.AllStrings(bp_marker_types))
    
    bp_map = {}
    for item in dssr_bp_types:
        bp_map[item] = item #'${}$'.format(item)
    
    
    magnification = max(1, min(len(dssrids)/40, 10))
    edges = []
    bp_markers = []

    for item in dssrout['pairs']:
        i1 = dssrids.index(item['nt1'])
        i2 = dssrids.index(item['nt2'])
        edges.append((i1, i2))
        style_dict[(i1, i2)] = ':'#'dashed'
        arrow_dict[(i1, i2)] = 0.001*magnification

        v = points[i1] - points[i2]
        d = np.linalg.norm(v)

        if d < 2: ## do not show bp type for too small edges
            continue
        p = points[i2]+v/2 
        typ = item['Saenger'].split("-")[0]
        
        if typ not in dssr_bp_types: # DSSR couldn't determine properly
            continue
        orient = 'w'
        bp_markers.append([p, bp_map[typ], orient, typ])

        
    return edges, bp_markers, bp_map


def getBasePairingEdges(dssrout, dssrids, points):
    
    #bp types: DSSR [ct][MWm][+-][MWm]
    dssr_bp_types = list(sre_yield.AllStrings('[MWm][MWm]'))
    dssr_bp_types.remove("WW")
    bp_marker_types = '[o^pdshP*]'
    marker_bp_types = list(sre_yield.AllStrings(bp_marker_types))
    
    bp_map = {}
    for item in dssr_bp_types:
        bp_map[item] = marker_bp_types[dssr_bp_types.index(item)]
    
    # print(bp_map)
    
    magnification = max(1, min(len(dssrids)/40, 10))
    edges = []
    bp_markers = []

    for item in dssrout['pairs']:
        i1 = dssrids.index(item['nt1'])
        i2 = dssrids.index(item['nt2'])
        edges.append((i1, i2))
        style_dict[(i1, i2)] = ':'#'dashed'
        arrow_dict[(i1, i2)] = 0.001*magnification

        v = points[i1] - points[i2]
        d = np.linalg.norm(v)

        if d < 2: ## do not show bp type for too small edges
            continue
        p = points[i2]+v/2 
        typ = item['DSSR'][1]+ item['DSSR'][3]
        
        if "." in typ: # DSSR couldn't determine properly
            continue
        if typ == "WW": #do not show watson crick pairs
            continue
        if item['DSSR'][0] == 'c':
            orient = 'k'
        else:
            orient = 'w'
        bp_markers.append([p, bp_map[typ], orient, item['DSSR'][0]+typ])

        
    return edges, bp_markers, bp_map

def getBackBoneEdges(ids, chids, dssrids, dssrout):

    magnification = max(1, min(len(ids)/40, 10))
    edges = []
    for i in range(len(dssrids) -1):
        _,_,_, chid1 = process_resid(dssrout['nts'][i]["nt_id"])
        _,_,_, chid_next = process_resid(dssrout['nts'][i+1]["nt_id"])
        
        try:
            if chid1 == chid_next:
                a = dssrids.index(dssrout['nts'][i]["nt_id"])
                b = dssrids.index(dssrout['nts'][i+1]["nt_id"])
                edges.append((a,b))
                style_dict[(a,b)] = 'solid'
                arrow_dict[(a,b)] = 10*np.sqrt(magnification)
        except:
            pass
    
    return edges

def Plot(points, markers, ids, chids, dssrids, dssrout, prefix="", rotation=False, bp_type='DSSR',
        out_path=None, time_string="ac1", extra={'arrowsize':1, 'circlesize':1,
            'circle_labelsize':1, 'cols':['#FF9896', '#AEC7E8', '#90CC84', '#DBDB8D', '#FFFFFF']
            }):
    '''rotation is False if no rotation is wished, otherwise, one
    can a pass a value in radian e.g. np.pi , np.pi/2, np.pi/3 etc. '''
    dssrids = list(dssrids) # for npz
    rotation_string = "" # used to append to file name
    if not rotation:
        pass
    else:
        rotation_string = str(rotation)
        rotation = np.radians(float(rotation))
        centroid = np.mean(points, axis=0)
        V = points - centroid
        theta = -1*rotation
        rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        V_ = np.dot(rot, V.T).T
        points = centroid + V_

    magnification = max(1, min(len(points)/40,10))
    G = nx.DiGraph()
    cold = {'A': extra['cols'][0],#'#FF9896',#'#90cc84',
    'C': extra['cols'][3],#'#DBDB8D',#'#AEC7E8',
    'G': extra['cols'][2],#'#90cc84',#'#DBDB8D',
    'U': extra['cols'][1],#AEC7E8',#'#FF9896',
    'DA': extra['cols'][0],#'#FF9896',#'#90cc84',
    'DC': extra['cols'][3],#'#DBDB8D',#'#AEC7E8',
    'DG': extra['cols'][2],#'#90cc84',#'#DBDB8D',
    'DT': extra['cols'][1],#'#AEC7E8'#'#FF9896'
    }

    colors = []
    labels = {}
    for i, (point, marker) in enumerate(zip(points, markers)):
        G.add_node(i, pos=point)
        marker = marker.replace("$","")
        
        if marker in cold.keys():
            labels[i] = marker[-1]
        else:
            #print(chem_components['0MC'])
            if marker in chem_components.keys():
                parent = chem_components[marker].tolist()
                labels[i] = parent[-1].lower()
            else:
                labels[i] = 'X'
        try:
            colors.append(cold[marker])
        except:
            colors.append(extra['cols'][4])
    

    fig, ax = plt.subplots(1, figsize=(8*magnification, 6*magnification))
    
    
    #### draw edges #######
    if bp_type == "dssr":
        pairings, bp_markers, bp_map = getBasePairingEdges(dssrout, dssrids, points)
    elif bp_type == "saenger":
        pairings, bp_markers, bp_map = getBasePairingEdgesSaenger(dssrout, dssrids, points)
    elif bp_type == "rnaview":
        pairings, bp_markers, bp_map = getBasePairingEdgesRnaview(points, ids, chids, out_path=out_path)
    elif bp_type == "dssrLw":
        pairings, bp_markers, bp_map = getBasePairingEdgesDssrLw(dssrout, dssrids, points)

    for item in pairings:
        G.add_edge(item[0],item[1])
    

    edges = getBackBoneEdges(ids, chids, dssrids, dssrout)
    for item in edges:
        G.add_edge(item[0],item[1])

    d = deepcopy(G.edges)
    for item in d:
        if(points[item[0]][0] == points[item[1]][0]):
            #G.nodes[item[0]]['pos'] = (G.nodes[item[0]]['pos'] + np.random.random(2)*5)
            G.remove_edge(item[0],item[1])
    style = [style_dict[item] for item in G.edges]
    arrow = [arrow_dict[item]*extra['arrowsize'] for item in G.edges]
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=False,
            node_size=160*magnification*extra['circlesize'],
            edgelist=[],
            node_color=colors, edgecolors='#000000')
    nx.draw_networkx_labels(G, nx.get_node_attributes(G, 'pos'), labels,
            font_size=(10+(magnification))*extra['circle_labelsize'])
    nx.draw_networkx_edges(G, nx.get_node_attributes(G, 'pos'), style=style,
            arrowsize=arrow, width=1*magnification)
    
    if bp_type == "dssr":
        for item in bp_markers:
            plt.scatter(item[0][0], item[0][1], marker=item[1], color=item[2], s = 80*magnification,
                    linewidth=1*magnification, edgecolor='k', label=item[3] )
    elif bp_type == "saenger":
        for item in bp_markers:
            plt.text(item[0][0], item[0][1], item[1], color='k', fontsize=10*np.sqrt(magnification))
    
    elif bp_type == "rnaview" or bp_type == "dssrLw":
        for item in bp_markers:
            if(item[1] == "ss" or item[1] == ">>"): # just need one shape for these
                plt.scatter(item[0][0][0], item[0][0][1], marker=getCustomMarker(0, item), color=item[2], s = 80*magnification,
                    linewidth=1*magnification, edgecolor='k', label=item[3] )
            else:
                # first shape!
                plt.scatter(item[0][1][0], item[0][1][1], marker=getCustomMarker(0, item), color=item[2], s = 80*magnification,
                    linewidth=1*magnification, edgecolor='k', label=item[3] )
                
                # second shape!
                plt.scatter(item[0][2][0], item[0][2][1], marker=getCustomMarker(1, item), color=item[2], s = 80*magnification,
                    linewidth=1*magnification, edgecolor='k', label=item[3] )        

    '''
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), title="non-WC bps")
    '''
    plt.tight_layout()
    plt.gca().set_aspect('equal')
    plt.savefig('{}/{}/{}{}{}.png'.format(MEDIA_PATH,FIG_PATH,prefix,time_string, rotation_string))
    plt.savefig('{}/{}/{}{}{}.svg'.format(MEDIA_PATH,FIG_PATH,prefix,time_string, rotation_string))

    plt.close()


    # SAVE JSON of pertinent information to call regenerate labels!
    # maybe also print time string

    # for item in bp_map.keys():
    #     plt.scatter(0,0,marker=bp_map[item], color='k', label = 'c'+item, linewidth=1,
    #             edgecolor='k')
    #     plt.scatter(0,0,marker=bp_map[item], color='w', label = 't'+item, edgecolor='k',
    #             linewidth=1)
    # plt.legend()
    # plt.savefig('{}/{}/legend.svg'.format(MEDIA_PATH,FIG_PATH))

    # return '{}/{}{}{}.png'.format(FIG_PATH,prefix,time_string,rotation_string)
    return '{}/{}{}{}.svg'.format(FIG_PATH,prefix,time_string,rotation_string), '{}/{}{}{}.png'.format(FIG_PATH,prefix,time_string,rotation_string)


