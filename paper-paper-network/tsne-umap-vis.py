import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as plt3d
#import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
import math
from sklearn.metrics import euclidean_distances, pairwise_distances
from sklearn import manifold
import matplotlib.lines as mlines
import pandas as pd
import umap
import numpy as np
import sys

from distancematrix import get_dist_matrix


def drawing(outfilename, pos):
	np.savetxt(outfilename+".csv", pos, delimiter=",")
	fig = plt.figure()
	ax = plt.axes()
	ax.grid(False)
	plt.axis('off')
	ax.scatter(pos.T[0], pos.T[1],  c='green', marker="." ,  cmap='Greens');
	plt.savefig(outfilename)






filepath="npstem100000.csv"
samples=10000
D1=get_dist_matrix(filepath, samples)

print(D1.shape)
#import pdb; pdb.set_trace()
 
pr=20
ex=12
lr=200

outfilename="papers_" + str(samples)+ "tsne_perplexity_"+str(pr)+".pdf"
#tsne = manifold.TSNE(n_components=3,perplexity=10.0, early_exaggeration=12.0, learning_rate=200.0, n_iter=1000, n_iter_without_progress=300, min_grad_norm=1e-07, metric='euclidean', init='random', verbose=1, random_state=None, method='barnes_hut', angle=0.5)

tsne = manifold.TSNE(n_components=2,perplexity=pr, early_exaggeration=ex, learning_rate=lr, n_iter=1000, n_iter_without_progress=300, min_grad_norm=1e-07, metric='euclidean', init='random', verbose=1, random_state=None, method='barnes_hut', angle=0.5)
pos = tsne.fit_transform(D1) #fit(similarities).embedding_
drawing(outfilename, pos)

 
n_neighbors=5
outfilename="paper_"+str(samples)+"_umap_neighbors_" + str(n_neighbors) +".png"

posumap = umap.UMAP(n_neighbors=n_neighbors,
                      min_dist=0.3,
                      metric='euclidean').fit_transform(D1)
drawing(outfilename, posumap)
