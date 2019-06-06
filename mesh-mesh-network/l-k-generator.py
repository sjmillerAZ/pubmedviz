import numpy as np
import pandas as pd
import sys

from timeit import default_timer as timer
import sys
filename='edges.csv'
nodelist='nodelist.csv'
releasedir='release/'
#k=3000
k=int(sys.argv[1])
nodes=pd.read_csv(nodelist)

nodes.columns=['n', 'weight']
nodes=nodes[nodes['n']!='mesh_code']
nodes['ndot']=nodes['n'] +' [weight="'+ nodes['weight'].map(str)+'"];'
nodes=nodes['ndot']



edges=pd.read_csv(filename, header=None)
edges.columns=['src','dest', 'weight']
edges=edges[edges['weight']>k]
edges.to_csv(releasedir+'edgelist_weight_'+str(k)+'.csv', index=False)

edgeformat='{}--{} [weight="{}"];'
#edges['e']=edgeformat.format(edges['src'],edges['dest'],edges['weight'])
edges['e']=edges['src']+ '--'+ edges['dest']+' [weight="'+ edges['weight'].map(str)+'"];'

edges=edges['e']

f=open(releasedir+'edgelist_dot_'+str(k)+'.dot', 'w')

f.write("graph{ \n ")
np.savetxt(f, nodes, fmt='%s')
np.savetxt(f, edges, fmt='%s')
f.write("}")
f.close()



