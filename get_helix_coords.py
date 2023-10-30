from Bio.PDB import MMCIFParser
import Bio
import json
import re, os, sys
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

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
    if "^" in spl1[1]:
        tmp = spl1[1].split("^")[0]
        icode = spl1[1].split("^")[1]
        spl1[1] = tmp
    else:
        icode = ' ' 


    res1 = re.sub("\D",",",spl1[1]).split(",")[-1]
    
    rest1_n = untillastnumber(spl1[1])
    rest1 = spl1[1]
    
    if (rest1_n not in list('AUGC') + ['DA','DC','DG','DT']):
        het1 = 'H_' + rest1_n
    else:
        het1=' '

    return spl1, (het1.strip("/"), int(res1), icode), rest1.strip("/")


def get_helix_coords(dssrout, model):
    helices = []
    for helix in dssrout['helices']:
        helix_data = {
            'coords' : [],
            'markers' : [],
            'pairs' : [],
            'ids':[]
        }
        for pair in helix['pairs']:
            nt1 = pair['nt1']
            nt2 = pair['nt2']
            
            spl1, id1, rest1 = process_resid(nt1)
            spl2, id2, rest2 = process_resid(nt2)
            ntc1 = get_cetroid(model[spl1[0]][id1])
            ntc2 = get_cetroid(model[spl2[0]][id2])
            #    sys.exit()
            
            #coords.append((ntc1+ntc2)/2)

            helix_data['coords'].append(ntc1)
            helix_data['coords'].append(ntc2)
            helix_data['markers'].append("${}$".format(rest1))
            helix_data['markers'].append("${}$".format(rest2))
            helix_data['pairs'].append((rest1, rest2))
            helix_data['ids'].append(id1)
            helix_data['ids'].append(id2)
             
            #coords.append((ntc1+ntc2)/2)
        helices.append(helix_data)

    coords = []
    markers = []

    ids = []

    for item in helices:
        coords += item['coords']
        markers += item['markers']
        ids += item['ids']

    pca = PCA(n_components=2)        
    pcs = pca.fit_transform(np.array(coords))

    '''
    for i in range(len(markers)):
        plt.scatter(pcs[i,0], pcs[i,1], marker=markers[i], edgecolors='none', color='black', s=100)

    #plt.show()
    #plt.close()
    '''
    def transformHelix(helix, style="heur"):
        pc2 = pca.transform(helix['coords'])
        if style == "center":
            pc1 = []
            for i in range(len(pc2)):
                if i%2==1:
                    pass
                else:
                    center = (pc2[i,:] + pc2[i+1,:])/2
                    pc1.append(center)
            #   l = pcs[i,:] - center
            #   print(l, np.linalg.norm(l))
        elif style == "polyfit":
            pc1 = []
            p = np.polyfit(pc2[:,0],pc2[:,1],deg=1)
            for item in pc2:
                pc1.append([item[0], item[0]*p[0] + p[1]])
        elif style == "pc":
            p = PCA(n_components=2)
            pc1 = p.fit_transform(pc2).tolist()
        elif style=="heur":
            first = (pc2[0] + pc2[1])/2
            last = (pc2[-1] + pc2[-2])/2
            n = len(pc2)//2
            pc1=[first]
            #print(n)
            for i in range(n-1):
                p = first + (i+1)*(last - first)/(n-1)
                pc1.append(p)
            #print(len(pc1))
        return pc1

    helix_axes = []
    for item in helices:
        helix_axes += [transformHelix(item)]

    def processHelixAxes(helix_axes):
        axes = []

        toalign = []
        for axis in helix_axes:
            last = axis[-1]
            if toalign == []:
                toalign.append([axis])
                continue
            else:
                prev = toalign[-1][-1]
                prelast = prev[-1]
                predir = prev[-1] - prev[-2]
                predir = predir/np.linalg.norm(predir)
                first = axis[0]
                #sys.exit()
                currdir = axis[1] - axis[0]
                currdir = currdir/np.linalg.norm(currdir)
                deviation = np.arccos(np.dot(predir,currdir))

                if np.linalg.norm(first - prelast) < 20: #(check if within certain distance)
                    #print("here!!!", deviation)
                    if deviation < 3.14/5: # check if axis deviation less than pi/6 (30 degrees)
                        toalign[-1].append(axis)
                    else:
                        toalign.append([axis])
                else:
                    toalign.append([axis])
            axes += axis
        aligned = []
        for item in toalign:
            if len(item) == 1:
                aligned+=item
                continue
            alll = []
            for ax in item:
                alll+=ax
            first = alll[0]
            last = alll[-1]
            n = len(alll)
            toappend = [first]
            for i in range(n-1):
                p = first + (i+1)*(last - first)/(n-1)
                toappend.append(p)
            aligned += [toappend]
        return aligned

    helix_axes= processHelixAxes(helix_axes)
    #helix_axes = np.array(helix_axis)
    #print(helix_axis.shape)
    '''
    for helix_axis in helix_axes:
        for i in range(len(helix_axis)):
            d = np.array(helix_axis)
            plt.scatter(d[i,0], d[i,1], edgecolors='none', color='black', s=100)
    plt.show()
    plt.close()
    '''
    points = []

    d = 3.5
    for helix_axis in helix_axes:   
        for i in range(len(helix_axis)-1):
            local_axis = (helix_axis[i+1] - helix_axis[i])
            local_axis_3ded = np.array(local_axis.tolist() + [0])
            zaxis = np.array([0,0,1])
            local_perp = np.cross(local_axis_3ded, zaxis)[:2]
            local_perp = local_perp/np.linalg.norm(local_perp)
            p1 = helix_axis[i] + local_perp*d
            p2 = helix_axis[i] - local_perp*d
            points += [p2, p1]


        last_point1 = points[-2] + helix_axis[-1] - helix_axis[-2]
        last_point2 = points[-1] + helix_axis[-1] - helix_axis[-2]
        #print(last_point1, last_point2)

        points += [last_point1, last_point2]
    points = np.array(points)
    
    '''
    for i in range(len(markers)):
        plt.scatter(points[i,0], points[i,1], marker=markers[i], edgecolors='none', color='black', s=100)
    plt.show()
    '''
    return points, ids, markers

if __name__ == "__main__":
    prefix = sys.argv[1]
    parser = MMCIFParser()
    model = parser.get_structure(prefix,"./vn/{}-assembly1.cif".format(prefix))[0]

    with open("./{}.json".format(prefix),"r") as f:
        dssrout = json.load(f)

    get_helix_coords(dssrout, model)



