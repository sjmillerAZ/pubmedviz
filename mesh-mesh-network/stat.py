import networkx as nx
import sys
import pygraphviz as pgv
from networkx.drawing.nx_agraph import write_dot
ks=[10000,5000,4000,3000,2000,1000,500]
print ("graph, nodes,edges,average_degree,  nodes,edges,average_degree  \n")
for k in ks:
	graphformat="release/edgelist_dot_{}.dot"
	G=nx.Graph(pgv.AGraph(graphformat.format(k)))

	Gc=max(nx.connected_component_subgraphs(G),key=len)

	
	 
	l="(2,{})-MeSH & {} & {}  & {:.2f} & {}  & {} & {:.2f}\\\ \hline"
	l_text=l.format(k,len(G.nodes()), len(G.edges()),  len(G.edges())/len(G.nodes()) , len(Gc.nodes()), len(Gc.edges()),  len(Gc.edges())/len(Gc.nodes()) )
	print ( l_text)

#	print (graphformat.format(k)+"[max]", len(Gc.nodes()), len(Gc.edges()), len(Gc.edges())/len(Gc.nodes()))
	write_dot(Gc,"max/release/max_component_"+str(k)+".dot") 
	



