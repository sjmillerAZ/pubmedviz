# This repository generates MeSH-MeSH network for PubMed paper-Mesh network.

`Caution`: parallel computing environment is required for this repository. The code was tested in `High Performance Computing System (HPC)` of the University of Arizona. This network data with `234M edges` was processed with `72 CPUs`.

# Data
```
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
```

## computing MeSH node weight
### 1. take mesh_code column and save as new file to
```console
$ cut -d, -f2 crest_full_set.12.05.2016.csv > cfset_f2.csv
```

### 2. run python code in parallel computing envionment
```console
$ mpirun -n 72 python3 weight_counter.py it produces output file aggcfset_f2.csv
$ more aggcfset_f2.csv

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

$ cp aggcfset_f2.csv  nodelist.csv
```
### 3. run mesh to mesh edge creator see the algorithm in draft paper
```console
$ mpirun -n 72 python3 edge_creator_un.py
```
output is saved as `edges.csv`

### 4. apply l-k threshold with k command line parameter
```console
$ python3 l-k-generator.py 5000
```
output saved as graph `dot` formate in `release` directory

### compute some statistics of the generated graphs
```console
6. run stat.py to get stastics of generated l-k meshnetwork
```
