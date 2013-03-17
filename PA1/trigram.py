import sys
from math import log
traindata = open('gene.count').readlines()
testdata = open('gene.dev').readlines()
outfp = open('gene_dev.p2.out','w')
wordfreq = {}
gram_freq = [{},{},{},{} ] 
tag_list = []
def updatedict(_dict,_key,_add):
	if not _dict.has_key(_key):
		_dict[_key]=_add
	else:
		_dict[_key]+=_add
def initdict():
	tag_list= []
	for line in traindata:
		l = line.replace('\n','').split(' ')
		if l[1]=='WORDTAG':
			count=int(l[0])
			tag =l[2]
			word = l[3]
			if not wordfreq.has_key(word):
				wordfreq[word]={}
			updatedict(wordfreq[word],tag,count)
		else:
			grams=int(l[1][0])
			count=int(l[0])
			tmp = l[2:2+grams]
			gram_freq[grams][tuple(tmp)]=count
			if grams==1:
				tag_list.append(l[2])
	tag_list.append('*')
	tag_list.append('STOP')
def tr(word):
	if not wordfreq.has_key(word):
		return "_RARE_"
	else:
		return word

def q(yi,yi_1,yi_2):
	return gram_freq[3][(yi,yi_1,yi_2)]*1.0/gram_freq[2][(yi_1,yi_2)]

def e(word,tag):
	word=tr(word)
	return wordfreq[word][tag]*1.0/gram_freq[1][tag]

initdict()

def veterbi(sentence):
	dp={}
	p={}
	sentence.append('STOP')
	p[(0,'*','*')]=(0,'*','*')
	dp[(0,'*','*')]=0
	for i in range(1,len(sentence)+1):
		word = sentence[i]
		for yi in tag_list:
			for yi_1 in tag_list:
				for yi_2 in tag_list:





