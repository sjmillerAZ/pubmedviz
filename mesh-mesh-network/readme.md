Data
# more crest_full_set.12.05.2016.csv
pmid,mesh_code
6511629,D008297
6511629,D007182
6511629,D006801
6511629,D005260
6511629,D005190
...
...
...


Weight count of each MeSH node
1. take mesh_code column and save as new file to 
cut -d, -f2 crest_full_set.12.05.2016.csv > cfset_f2.csv 

2. run  
mpirun -n 10 python3 weight_counter.py it produces output file aggcfset_f2.csv

#more aggcfset_f2.csv 

m,weight
D000001,11743
D000002,313
D000003,4846
D000004,1016
D000005,35699
D000006,8940
D000007,13414
D000008,8790
D000009,10432
...
...
...


3. cp aggcfset_f2.csv  nodelist.csv

4. run mesh to mesh edge creator see the algorithm 
mpirun -n 50 python3 edge_creator_un.py 
give output edges.csv

5. apply l-k threshold 
python3 l-k-generator.py 5000 

gives output as dot formate stored in release 


6. run stat.py to get stastics of generated l-k meshnetwork









