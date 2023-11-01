import networkx as nx
from matplotlib import pyplot as plt

plt.gca().invert_yaxis()
plt.gca().invert_xaxis()

style_dict = {}

def getBasePairingEdges(dssrout, dssrids):
    edges = []
    
    for item in dssrout['pairs']:
        i1 = dssrids.index(item['nt1'])
        i2 = dssrids.index(item['nt2'])
        edges.append((i1, i2))
        style_dict[(i1, i2)] = 'dashed'

    return edges

def getBackBoneEdges(ids, chids):
    edges = []
    for i in range(len(ids)):
        try:
            if chids[i] == chids[i+1]:
                edges.append((i,i+1))
                style_dict[(i,i+1)] = 'solid'
        except:
            pass
    return edges

def Plot(points, markers, ids, chids, dssrids, dssrout, prefix=""):
    G = nx.Graph()
    cold = {'A': '#90cc84',
    'C': '#AEC7E8',
    'G': '#DBDB8D',
    'U': '#FF9896'
    }
    colors = []
    labels = {}
    for i, (point, marker) in enumerate(zip(points, markers)):
        G.add_node(i, pos=point)
        marker = marker.replace("$","")
        
        if marker in cold.keys():
            labels[i] = marker
        else:
            labels[i] = 'X'
        try:
            colors.append(cold[marker])
        except:
            colors.append('#ffffff')
    
    fig, ax = plt.subplots(1, figsize=(16, 12))
    nx.draw(G, nx.get_node_attributes(G, 'pos'), with_labels=False,
            node_color=colors, edgecolors='#000000')
    nx.draw_networkx_labels(G, nx.get_node_attributes(G, 'pos'), labels)
    
    #### draw edges #######
    edges = getBackBoneEdges(ids, chids)
    for item in edges:
        G.add_edge(item[0],item[1])

    pairings = getBasePairingEdges(dssrout, dssrids)
    
    for item in pairings:
        G.add_edge(item[0],item[1])
    


    style = [style_dict[item] for item in G.edges]
    nx.draw_networkx_edges(G, nx.get_node_attributes(G, 'pos'), style=style)
            #v = v/np.linalg.norm(v)
    plt.savefig('{}nx.png'.format(prefix))

