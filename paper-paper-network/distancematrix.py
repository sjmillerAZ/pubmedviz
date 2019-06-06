import pandas as pd
import keras.preprocessing.text as text
import sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import euclidean_distances
from sklearn import preprocessing
import json

import numpy as np

def get_dist_matrix(f, n):

	#data=pd.read_csv("../data/exportingForML_full.csv",  dtype={'title': object, 'abs':object})
	data=pd.read_csv(f)
	data=data[0:n]
	vocab_size=50000
	tokenize = text.Tokenizer(num_words=vocab_size)
	tokenize.fit_on_texts(data['stem'].astype(str))
	M = tokenize.texts_to_matrix(data['stem'].astype(str))
	M=euclidean_distances(M)
	return M

#if __name__=="__main__":
#	filepath="npstem10000.csv"
#	M=get_dist_matrix(file, 1000)
	
	

