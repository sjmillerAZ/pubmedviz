
from mpi4py import MPI
import numpy as np
import pandas as pd
from timeit import default_timer as timer
import sys

def process_one_vertex(current_node,df):
	#current_node='D008875'
	filter_A_nodes=df[df['B']==current_node]['A']
	B=df[df['A'].isin(filter_A_nodes)]#['B']
	count=B.groupby(['B']).size().to_frame(name='c').reset_index()
	f=np.full( len(count), current_node)
	src=pd.DataFrame({'src':pd.Series(f)})
	edges=src.join(count)
	edges.columns=['src','dest','weight']
	edges=edges[edges['weight']>1]
	edges=edges[edges['dest']<current_node]
	
	return edges


st_index =int( sys.argv[1])
en_index = int(sys.argv[2])


	
#filename='1000000.csv'
#nodelistCSV='agg1000000f2.csv'
filename='crest_full_set.12.05.2016.csv'
nodelistCSV='nodelist.csv'

progressfile='progress.csv' #to keep track current progress 
df=pd.read_csv(filename, header=None)
df.columns=['A','B']
nodes=pd.read_csv(nodelistCSV)
nodes=nodes[st_index:en_index]
nodes.columns=['B','count']
progress=pd.read_csv(progressfile, header=None)
progress.columns=['B']
nodes=nodes[~nodes["B"].isin(progress)]

if len(nodes)==0:
	print(st_index, "--", en_index, ": This job is done")
	sys.exit()

comm=MPI.COMM_WORLD
rank =comm.Get_rank()
nprocs=comm.Get_size()

recperrank=int(len(nodes)/(nprocs-1))
if rank>0:
	st=timer()
	mynodes=nodes[(rank-1)*recperrank:rank*recperrank]['B'].reset_index()['B']
	e=pd.DataFrame({'src':[],'dest':[],'weight':[]})
	counter=0
	print("need to process:", recperrank)
	for current_node in mynodes:

		if counter%10==0: print("rank=", rank, " counter ",  counter)
		counter=counter+1
	#current_node='D019469'
		ei=process_one_vertex(current_node,df )
		ei.to_csv('output/'+current_node+'.csv', index=False, header=False)
		f= open('progress.csv', 'a')
		f.write(current_node+"\n")
		f.close()
		    
		e=e.append(ei)
		if rank==1:
			print("Single_rank:", rank, " counter: ",  counter, "time:", timer()-st )
		
	print("Rank:", rank, "Data size: ", len(e))
	comm.send(e, dest=0)
 
if rank==0:
	data=comm.recv(source=1)
	for i in range(2, nprocs):
		di=comm.recv(source=i)
		data=data.append(di)

	#c=data.groupby(['m'])['c'].agg('sum').to_frame(name='weight').reset_index()	
	data.to_csv('edges'+filename, index=False)
	

 


