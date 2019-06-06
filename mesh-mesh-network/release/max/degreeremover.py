import networkx as nx
import pygraphviz as pgv
from networkx.drawing.nx_agraph import write_dot
import pandas as pd
import os

lbl='../../data/crest_mesh_names.12.05.2016.csv'
nodelbl=pd.read_csv(lbl)

selectNumbersofHighDegreeNodes=100

outfile="10000_connection_top"

f='max_component_10000.dot'
G1=nx.Graph(pgv.AGraph(f))
G=nx.Graph(pgv.AGraph(f))

c=nx.degree_centrality(G)
s=sorted(c.items(), key=lambda x: x[1], reverse=True)
s=s[0:selectNumbersofHighDegreeNodes]
s_id=[si[0] for si in s]
for x in G.nodes():
    ll=nodelbl[nodelbl['mesh_code']==x].reset_index()
    l=ll['mesh_name'][0]
    G1.add_node(x,label=l)
    #import pdb; pdb.set_trace()
    if x not in s_id:
        G1.remove_node(x)




#for x in G.nodes():
#    if G.degree( x)<10:
#        G1.remove_node(x)

#print("Node Id & Node Name & Degree & Weight\\\ \hline")
#for x in s:
    #print(x[0])
#    ll=nodelbl[nodelbl['mesh_code']==x[0]].reset_index()
#    l=ll['mesh_name'][0]
#    txt="{} & {} & {} & {:.2f}M\\\ \\hline"
    #import pdb; pdb.set_trace()
#    print(txt.format(x[0],l, G.degree(x[0]),  int( G.nodes[x[0]]["weight"])/10**6  ))
    #G1[x[0]]={'label':l}
#    G1.add_node(x[0],label=l)
#    G1.remove_node(x[0])

write_dot(G1, outfile+".dot")
#os.system(' sfdp  -Goverlap=prism  '+ outfile+".dot -Tpdf > " + outfile +".pdf")
#print(len(G1), len(G1.edges()))
