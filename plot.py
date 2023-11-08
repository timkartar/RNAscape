import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import sre_yield
from config import FIG_PATH
from copy import deepcopy
from math import cos, sin

plt.gca().invert_yaxis()
plt.gca().invert_xaxis()
style_dict = {}
arrow_dict = {}

def getBasePairingEdges(dssrout, dssrids, points):
    
    #bp types: DSSR [ct][MWm][+-][MWm]
    dssr_bp_types = list(sre_yield.AllStrings('[MWm][MWm]'))
    dssr_bp_types.remove("WW")
    bp_marker_types = '[o^pdshP*]'
    marker_bp_types = list(sre_yield.AllStrings(bp_marker_types))
    
    bp_map = {}
    for item in dssr_bp_types:
        bp_map[item] = marker_bp_types[dssr_bp_types.index(item)]
    
    #print(bp_map)
    
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

def getBackBoneEdges(ids, chids, dssrids):

    magnification = max(1, min(len(ids)/40, 10))
    edges = []
    for i in range(len(ids)):
        try:
            if chids[i] == chids[i+1]:
                edges.append((i,i+1))
                style_dict[(i,i+1)] = 'solid'
                arrow_dict[(i,i+1)] = 10*np.sqrt(magnification)
        except:
            pass
    return edges

def Plot(points, markers, ids, chids, dssrids, dssrout, prefix="", rotation=False):
    '''rotation is False if no rotation is wished, otherwise, one
    can a pass a value in radian e.g. np.pi , np.pi/2, np.pi/3 etc. '''

    if not rotation:
        pass
    else:
        centroid = np.mean(points, axis=0)
        V = points - centroid
        theta = rotation #in radian 
        rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        V_ = np.dot(rot, V.T).T
        points = centroid + V_

    magnification = max(1, min(len(points)/40,10))
    G = nx.DiGraph()
    cold = {'A': '#FF9896',#'#90cc84',
    'C': '#DBDB8D',#'#AEC7E8',
    'G': '#90cc84',#'#DBDB8D',
    'U': '#AEC7E8',#'#FF9896',
    'DA': '#FF9896',#'#90cc84',
    'DC': '#DBDB8D',#'#AEC7E8',
    'DG': '#90cc84',#'#DBDB8D',
    'DT': '#AEC7E8'#'#FF9896'
    }

    colors = []
    labels = {}
    for i, (point, marker) in enumerate(zip(points, markers)):
        G.add_node(i, pos=point)
        marker = marker.replace("$","")
        
        if marker in cold.keys():
            labels[i] = marker[-1]
        else:
            labels[i] = 'X'
        try:
            colors.append(cold[marker])
        except:
            colors.append('#ffffff')
    

    fig, ax = plt.subplots(1, figsize=(8*magnification, 6*magnification))
    
    
    #### draw edges #######
    pairings, bp_markers, bp_map = getBasePairingEdges(dssrout, dssrids, points)
    
    for item in pairings:
        G.add_edge(item[0],item[1])
    

    edges = getBackBoneEdges(ids, chids, dssrids)
    for item in edges:
        G.add_edge(item[0],item[1])

    

    
    
    d = deepcopy(G.edges)
    for item in d:
        if(points[item[0]][0] == points[item[1]][0]):
            #G.nodes[item[0]]['pos'] = (G.nodes[item[0]]['pos'] + np.random.random(2)*5)
            G.remove_edge(item[0],item[1])
    style = [style_dict[item] for item in G.edges]
    arrow = [arrow_dict[item] for item in G.edges]
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=False, node_size=160*magnification,
            edgelist=[],
            node_color=colors, edgecolors='#000000')
    nx.draw_networkx_labels(G, nx.get_node_attributes(G, 'pos'), labels,
            font_size=10+(magnification))
    nx.draw_networkx_edges(G, nx.get_node_attributes(G, 'pos'), style=style,
            arrowsize=arrow, width=1*magnification)
    
    for item in bp_markers:
        plt.scatter(item[0][0], item[0][1], marker=item[1], color=item[2], s = 80*magnification,
                linewidth=1*magnification, edgecolor='k', label=item[3] )

    '''
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), title="non-WC bps")
    '''
    plt.tight_layout()
    plt.gca().set_aspect('equal')
    plt.savefig('{}/{}.png'.format(FIG_PATH, prefix))
    plt.close()

    
    '''
    for item in bp_map.keys():
        plt.scatter(0,0,marker=bp_map[item], color='k', label = 'c'+item, linewidth=1,
                edgecolor='k')
        plt.scatter(0,0,marker=bp_map[item], color='w', label = 't'+item, edgecolor='k',
                linewidth=1)
    plt.legend()
    plt.savefig('{}/legend.png'.format(FIG_PATH))
    '''
