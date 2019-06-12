# This repository generates maps for mediline abstracts. (data is not included)
`Caution`: The code was tested in `High Performance Computing System (HPC)` of the University of Arizona using docker `https://hub.docker.com/r/hossain/gdocker`

# Step1: take noun phrases and stemming abstracts
```console
$ python3 txtprocessor.py
```
## Step2: find tsne and umap embedding
```console
$ python3 tsne-umap-vis.py
```
## Step3: find k-nearest neighbor and export as graph `dot`
```console
$ python k-neighbor_and_make_dot.py
```

## Step4: apply clustering, give map look and get drawing as `svg`
```console
$eba/kmeans -action=clustering -C=geometrickmeans dot.dot > out1.dot
$gvmap -e  -c 1 out1.dot > out2.dot
$neato -Gforcelabels=false -Ecolor=grey -Gstart=123  -n2 -Tsvg  out2.dot > map.svg
```
## Step5: get ready meshname for selected abstracts for the visualization  
```console
$ run papermeshname.py
```
