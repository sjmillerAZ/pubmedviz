import numpy as np
import pandas as pd
import sys

import networkx as nx
import pygraphviz as pgv

from timeit import default_timer as timer
import sys
papermeshlinkfile='../data/medline_mesh-2015/medline_mesh_links-2015.csv'
meshnamefile='../data/medline_mesh_names-all.csv'
nodelist='npstem10000.csv'
outfile='papermeshname.csv'

meshnetworkfile='10000_connection_top.dot'
meshnetwork=nx.Graph(pgv.AGraph(meshnetworkfile))
expectednodes=meshnetwork.nodes()
expectednodes=[x for x in expectednodes]

papermesh=pd.read_csv(papermeshlinkfile)
nodes=pd.read_csv(nodelist)
meshname=pd.read_csv(meshnamefile)

papermesh=papermesh[papermesh["pmid"].isin(nodes["pmid"])]
papermesh=papermesh[papermesh["mesh_code"].isin(expectednodes)]


#papermesh=papermesh[papermesh["is_major_topic"]=='Y']
papermesh=papermesh[papermesh["is_geographic_topic"]=='N']
papermesh=papermesh[['pmid','mesh_code','is_major_topic']]

data=papermesh.join(meshname.set_index('mesh_code'), on='mesh_code')
data=data[['pmid','mesh_code','mesh_name','is_major_topic']]

data.to_csv(outfile, index=False)
 

