import os
from gensim.models import Word2Vec
import os.path

def get_word_pairs(dir_name):
	word_pairs = []
	files = os.listdir(dir_name)
	for filename in files:
		ifile = open(dir_name + '/' + filename, encoding="utf8")
		c = 0
		for l in ifile:
			if c == 0:
				c += 1
				continue
			window_size = 5
			words = l.split(' ')
			for i in range(len(words)):
				start_idx = i - 5
				if start_idx < 0:
					start_idx = 0
				end_idx = i + 5
				if end_idx > len(words):
					end_idx = len(words)
				for j in range(start_idx,end_idx,1):
					word_pairs += [[words[i],words[j]]]
		ifile.close()
	return word_pairs

def get_sentences(dir_name):
	sentences = []
	files = os.listdir(dir_name)
	n = 0
	for filename in files:
		n += 1
		if n > 1500:
			break
		ifile = open(dir_name + '/' + filename, encoding="utf8")
		c = 0
		for l in ifile:
			if c == 0:
				c += 1
				continue
			sentences += [l.split(' ')]
		ifile.close()
	return sentences


dir_name = 'crawl'
fname = 'word2vec.model'
if not os.path.isfile(fname):
	sentences = get_sentences(dir_name)
	model = Word2Vec(sentences, size=300,window=5,min_count=1)
	model.save(fname)
	print('model complete')

model = Word2Vec.load(fname)
while(True):
	word = input("Please enter query word : ")
	word = word.title()
	if word == 'exit':
		break
	if word in model.wv.vocab:
		simwords = model.most_similar(word,topn=10)
		s = []
		for (w,p) in simwords:
			s += [w]
		print('similar context : ' + str(s))
	else:
		print('Word not in the vocabulary. Please try again')



