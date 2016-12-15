import pickle
from nltk.corpus import stopwords
sentidx_words = pickle.load(open("tokenize.p", "rb"))
for tup in sentidx_words:
	for idx, word in enumerate(tup[1]):
		if word in stopwords.words('english'):
			del tup[1][idx]
pickle.dump(sentidx_words, open("stopwords_removed.p", "wb"))