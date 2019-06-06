run txtprocessor.py
run tsne-umap-vis.py
run k-neighbor_and_make_dot.py



~/external/eba/kmeans -action=clustering -C=geometrickmeans dot.dot > out1.dot
gvmap -e  -c 1 out1.dot > out2.dot
neato -Gforcelabels=false -Ecolor=grey -Gstart=123  -n2 -Tsvg  out2.dot > map.svg

run papermeshname.py
