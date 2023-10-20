from Bio.PDB import MMCIFParser
import Bio
import json
import re, os, sys
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

parser = MMCIFParser()
model = parser.get_structure("7vnv","./vn/7vnv-assembly1.cif")[0]

with open("./7vnv.json","r") as f:
    dssrout = json.load(f)

helical_coordinates=[]

def get_cetroid(res):
    atoms = []
    for atom in res:
        atoms.append(atom.coord)
    return np.mean(atoms, axis=0)

def untillastnumber(l):
    revl = l[::-1]
    
    for idx in range(len(revl)):
        if not revl[idx].isdigit():
            break
    return revl[idx:][::-1]

def process_resid(nt1):
    spl1 = nt1.split(".")
    res1 = re.sub("\D",",",spl1[1]).split(",")[-1]
    
    rest1 = untillastnumber(spl1[1])

    if (rest1 not in list('AUGC') + ['DA','DC','DG','DT']):
        het1 = 'H_' + rest1
    else:
        het1=' '
    return spl1, (het1, int(res1), ' '), rest1

coords = []
markers = []
for helix in dssrout['helices']:
    for pair in helix['pairs']:
        nt1 = pair['nt1']
        nt2 = pair['nt2']
        
        spl1, id1, rest1 = process_resid(nt1)
        spl2, id2, rest2 = process_resid(nt2)
        ntc1 = get_cetroid(model[spl1[0]][id1])
        ntc2 = get_cetroid(model[spl2[0]][id2])
        #    sys.exit()
        
        #coords.append((ntc1+ntc2)/2)

        coords.append(ntc1)
        coords.append(ntc2)
        markers.append("${}$".format(rest1[-1]))
        markers.append("${}$".format(rest2[-1]))

        
        #coords.append((ntc1+ntc2)/2)

pca = PCA(n_components=2)        
pcs = pca.fit_transform(np.array(coords))

for i in range(len(markers)):
    plt.scatter(pcs[i,0], pcs[i,1], marker=markers[i], edgecolors='none', color='black', s=100)

plt.show()
