import sys
traindata = open('gene.count').readlines()
testdata = open('gene.dev').readlines()
outfp = open('gene_dev.p1.out','w')
tagfreq = {}
wordfreq = {}
wordtag = {}
def updatedict(_dict,_key,_add):
	if not _dict.has_key(_key):
		_dict[_key]=_add
	else:
		_dict[_key]+=_add
def genfreqdict():
	for line in traindata:
		l = line.replace('\n','').split(' ')
		if l[1]=='WORDTAG':
			count=int(l[0])
			tag =l[2]
			word = l[3]
			if not wordfreq.has_key(word):
				wordfreq[word]={}
			updatedict(tagfreq,tag,count)
			updatedict(wordfreq[word],tag,count)

def genwordtag():
	for word in wordfreq:
		tagdict = wordfreq[word]
		tag = ""
		emission = 0.00
		for item in tagdict:
			tmp = tagdict[item]*1.00/tagfreq[item]
			if tmp>emission:
				tag=item
				emission=tmp
		wordtag[word]=tag		

genfreqdict()
genwordtag()

for line in testdata:
	s = line.replace('\n','')
	if s=='':
		outfp.write('\n')
		continue
	key = s
	if not wordfreq.has_key(s):
		key='_RARE_'
	outfp.write(s+' '+wordtag[key]+'\n')	
		
