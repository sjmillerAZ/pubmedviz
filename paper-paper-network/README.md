# This repository generates maps for mediline abstracts. (data is not included)
`Caution`: The code was tested in `High Performance Computing System (HPC)` of the University of Arizona using docker `https://hub.docker.com/r/hossain/gdocker`


```console
$ sort -k 5 -t ',' -r -g medlinex_cite_count_full.csv  > medlinex_cite_count_full_sorted.csv
$ more medlinex_cite_count_full.csv | grep ",2015" > cite_2015.csv
$ sort -k 5 -t ',' -r -g cite_2015.csv  > cite_2015_sorted.csv
$ head -n 10000 cite_2015_sorted.csv > cite_head_2015_10000.csv

```


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
