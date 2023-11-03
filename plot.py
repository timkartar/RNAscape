import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import sre_yield
plt.gca().invert_yaxis()
plt.gca().invert_xaxis()

style_dict = {}
arrow_dict = {}
def getBasePairingEdges(dssrout, dssrids, points):
    
    #bp types: DSSR [ct][MWm][+-][MWm]
    #dssr_bp_types = list(sre_yield.AllStrings('[ct][MWm][+-][MWm]'))
    dssr_bp_types = list(sre_yield.AllStrings('[MWm][MWm]'))
    
    #bp_marker_types = '[o^dshP][o^dshP]'
    bp_marker_types = '[o^pdshPH*]'
    marker_bp_types = list(sre_yield.AllStrings(bp_marker_types))
    
    bp_map = {}
    for item in dssr_bp_types:
        bp_map[item] = marker_bp_types[dssr_bp_types.index(item)]
    
    #print(bp_map)
    
    magnification = max(1, len(dssrids)/80)
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
        bp_markers.append([p, bp_map[typ], orient])

        
    return edges, bp_markers

def getBackBoneEdges(ids, chids, dssrids):

    magnification = max(1, len(ids)/80)
    edges = []
    for i in range(len(ids)):
        try:
            if chids[i] == chids[i+1]:
                edges.append((i,i+1))
                style_dict[(i,i+1)] = 'solid'
                arrow_dict[(i,i+1)] = 10*magnification
        except:
            pass
    return edges

def Plot(points, markers, ids, chids, dssrids, dssrout, prefix=""):
    
    magnification = max(1, len(points)/80)
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
    

    fig, ax = plt.subplots(1, figsize=(12*magnification, 9*magnification))
    
    
    #### draw edges #######
    pairings, bp_markers = getBasePairingEdges(dssrout, dssrids, points)
    
    for item in pairings:
        G.add_edge(item[0],item[1])
    

    edges = getBackBoneEdges(ids, chids, dssrids)
    for item in edges:
        G.add_edge(item[0],item[1])

    

    style = [style_dict[item] for item in G.edges]
    arrow = [arrow_dict[item] for item in G.edges]
    
    for item in G.edges:
        if(points[item[0]][0] == points[item[1]][0]):
            print(item, dssrids[item[0]], dssrids[item[1]])
            #G.nodes[item[0]]['pos'] = (G.nodes[item[0]]['pos'] + np.random.random(2)*5)
    
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=False, node_size=160*magnification,
            edgelist=[],
            node_color=colors, edgecolors='#000000')
    nx.draw_networkx_labels(G, nx.get_node_attributes(G, 'pos'), labels, font_size=10)
    nx.draw_networkx_edges(G, nx.get_node_attributes(G, 'pos'), style=style, arrowsize=arrow, width=1*magnification)
    
    for item in bp_markers:
        plt.scatter(item[0][0], item[0][1], marker=item[1], color=item[2], s = 80*magnification,
                linewidth=1*magnification, edgecolor='k' )
    plt.tight_layout()
    plt.savefig('./fig/{}nx.png'.format(prefix))

