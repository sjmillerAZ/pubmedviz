from nltk import word_tokenize, pos_tag, ne_chunk
from nltk import RegexpParser
from nltk import Tree
import pandas as pd


from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
ps=PorterStemmer()

#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

filename="/extra/hossain/mesh/data/medline_mesh-2015/medline_publications-2015.csv"
numberofrec=100000
thresold=3


df=pd.read_csv(filename)
df=df[0:numberofrec]
# Defining a grammar & Parser
NP = "NP: {(<V\w+>|<NN\w?>)+.*<NN\w?>}"
chunker = RegexpParser(NP)

def get_continuous_chunks(text, chunk_func=ne_chunk):
    chunked = chunk_func(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []
    for subtree in chunked:
        if type(subtree) == Tree:
            current_chunk.append(" ".join([token for token, pos in subtree.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    return continuous_chunk


 
df['text']=df['article_title'].astype(str) + " " + df["abstract_text"].astype(str) 

df['np']=df['text'].apply(lambda sent: get_continuous_chunks(sent, chunker.parse))

stemtxt=[]

for i in range(0, len(df)):
	txt=' '.join(df['np'][i]).split(" ")
	stext= [ps.stem(t) for t in txt ]
	stext=[ k for k in stext if len(k)>thresold ]
	a=' '.join(stext)
	stemtxt.append(a)
	if i % 500:
		print("progress " , i , "out of ", numberofrec , " \r", end='')

df['stem']=stemtxt	
savestemdf=df[['pmid','stem']]
outfilename="npstem"+str(numberofrec)+".csv"
savestemdf.to_csv(outfilename,index=False)
print("Done processing. File saved:", outfilename )	 
#import pdb; pdb.set_trace()



