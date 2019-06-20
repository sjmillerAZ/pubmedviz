import networkx as nx
from sklearn.neighbors import NearestNeighbors
import pandas as pd
from networkx.drawing.nx_agraph import write_dot



import matplotlib.pyplot as plt

import matplotlib.lines as mlines

scalingfactor=1000

pos_csv="papers_10000tsne_perplexity_20.pdf.csv"
pmid_file="npstem100000.csv"
pos=pd.read_csv(pos_csv, header=None)


 
numberofrec=10000
df=pd.read_csv(pmid_file)
df=df[0:numberofrec]

df["x"]=pos[0] * scalingfactor
df["y"]=pos[1] * scalingfactor
df=df[["pmid","x","y"]]



pos=pos.values

nbrs = NearestNeighbors(n_neighbors=4, algorithm='ball_tree').fit(pos)
distances, indices = nbrs.kneighbors(pos)





outfile="k-neigbor_" + str( numberofrec) + ".png"

fig = plt.figure()
ax = plt.axes()
ax.grid(False)
plt.axis('off')
ax.scatter(pos.T[0], pos.T[1],  c='green', marker="." ,  cmap='Greens');

'''

for x in indices:
	line = mlines.Line2D([pos[x].T[0]], [pos[x].T[1]], color='green')
	ax.add_line(line)
	
plt.savefig(outfile)

'''
node_attrb={}
G=nx.Graph()
for i in range(0, len(df)):
	n=str(df["pmid"][i])
	G.add_node(n)
	node_attrb[n]={"pos":"" + str( round(float(df["x"][i]),6)) + ","+ str( round(float(df["y"][i]),6)), "label":  n  }

nx.set_node_attributes(G, node_attrb)


for x in indices:
	for i in range(0, len(x)-1):
		n1=str(df["pmid"][x[i]])
		n2=str(df["pmid"][x[i+1]])
		G.add_edge(n1,n2)

write_dot(G,outfile+".dot")


