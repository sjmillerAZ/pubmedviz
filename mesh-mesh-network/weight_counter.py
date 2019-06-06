from mpi4py import MPI
import numpy as np
import pandas as pd


filename='1000000f2.csv'
#filename='cfset_f2.csv'
df=pd.read_csv(filename, header=None)
df.columns=['m']


comm=MPI.COMM_WORLD
rank =comm.Get_rank()
nprocs=comm.Get_size()

recperrank=int(len(df)/(nprocs-1))
if rank>0:
	mydata=df[(rank-1)*recperrank:rank*recperrank]
	count=mydata.groupby(['m']).size().to_frame(name='c').reset_index()
	print("Rank:", rank, "Data size: ", len(count))
	comm.send(count, dest=0)
 
if rank==0:
	data=comm.recv(source=1)
	for i in range(2, nprocs):
		di=comm.recv(source=i)
		data=data.append(di)
	c=data.groupby(['m'])['c'].agg('sum').to_frame(name='weight').reset_index()	
	c.to_csv('agg'+filename, index=False)
	

 


