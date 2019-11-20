import nltk
from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import RegexpParser
from nltk import Tree
import pandas as pd
import spacy
from nltk.stem import PorterStemmer
import numpy

nlp = spacy.load('en_core_web_sm')

from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps=PorterStemmer()

#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

filename="/Users/sjmiller/CourseCat/DataSciCourses_IDTitleFull.csv"
#maxrec=100000
maxrec=3
thresold=3

df=pd.read_csv(filename, nrows = maxrec)
print('Read %d lines' % df.shape[0])
maxrec = df.shape[0]
df=df[0:maxrec]

def processdata(data):

    doc = nlp(data)

    tokens = []
    for token in doc:
        if (token.is_alpha and not token.is_stop):
            stem = ps.stem(token.lemma_)
            if (len(stem) > 3):
                tokens.append(stem)

    return ' '.join(tokens)

#tst_str = "Course material includes Classification and characteristics of composite materials;"
#" mechanical behavior of composite materials, micro- and macro-mechanical behavior of laminae; mechanical behavior of laminates; mechanical behavior of short fiber composites."
#print(processdata(tst_str))
#exit()

df['text']=df['Course_Title'].astype(str) + " " + df["Full_Course_Description"].astype(str) 
df['stem']=df['text'].apply(processdata)

savestemdf=df[['CRSE_ID','stem']]
outfilename="coursecat_stem_"+str(maxrec)+".csv"
savestemdf.to_csv(outfilename,index=False)
print("Done processing. File saved:", outfilename )	 
#import pdb; pdb.set_trace()


dist = numpy.zeros((maxrec, maxrec))

def intersection(lst1, lst2): 
  
    # Use of hybrid method 
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3 

print(len(intersection(i,j) for i in df['stem'] for j in df['stem']) )
   

