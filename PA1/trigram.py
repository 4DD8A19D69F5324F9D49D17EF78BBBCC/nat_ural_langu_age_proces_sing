import sys
from math import log
traindata = open('gene.count').readlines()
testdata = open('gene.test').readlines()
outfp = open('gene_test.p2.out','w')
wordfreq = {}
gram_freq = [{},{},{},{} ] 
tag_list = []
inf = 1000000000000.0
def updatedict(_dict,_key,_add):
	if not _dict.has_key(_key):
		_dict[_key]=_add
	else:
		_dict[_key]+=_add
def initdict():
	global tag_list
	tag_list=['*']
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
			if grams >=2:
				gram_freq[grams][tuple(tmp)]=count
			if grams==1:
				tag_list.append(l[2])
				gram_freq[grams][l[2]]=count
def split_sentences(lines):
	ret = []
	tlist = []
	for line in lines:
		l = line.replace('\n','')
		if l=='':
			ret.append(tlist)
			tlist=[]
		else:
			tlist.append(l)
	if len(tlist)!=0:
		ret.append(tlist)
	return ret		

def q(c,b,a,pos=10):
	if c=='*' and b=='*' and pos!=0:
		return -inf
	if c=='*' and b!='*' and pos!=1:
		return -inf
	if (c,b,a) in gram_freq[3] and (c,b) in gram_freq[2]:
		return log(1.0*gram_freq[3][(c,b,a)]) - log(1.0*gram_freq[2][(c,b)])
	return -inf

def e(word,tag):
	if word !='*' and word != 'STOP' and word not in wordfreq:
		word='_RARE_'
	if word in wordfreq and tag in wordfreq[word]:
		return log(1.0*wordfreq[word][tag])-log(1.0*gram_freq[1][tag])
	return -inf
def gettag(sentence):
	dp= {}
	p = {}
	dp[(-1,'*','*')]=0
	p[(-1,'*','*')]=(-1,'*','*')
	for i in range(0,len(sentence)):
		word = sentence[i]
		for a in tag_list:
			for b in tag_list:
				val=-inf
				pre=(i,b,a)
				for c in tag_list:
					if (i-1,c,b) not in dp:
						continue
					tmp = dp[(i-1,c,b)]+q(c,b,a,i)+e(word,a)
					if tmp>val:
						val=tmp
						pre=(i-1,c,b)
				dp[(i,b,a)]=val
				p[(i,b,a)]=pre
	endidx=len(sentence)-1
	tmp=-inf
	last=(endidx,'ERROR','ERROR')
	for a in tag_list:
		for b in tag_list:
			if (endidx,b,a) in dp:
				val = q(b,a,'STOP') + dp[(endidx,b,a)]
				if val>tmp:
					tmp=val
					last=(endidx,b,a)
	ret = []
	for i in range(endidx,-1,-1):
		ret.append(last[2])
		last=p[last]
	ret.reverse()
	return ret


def test():
	print gram_freq[1]
	print gram_freq[2]
	print gram_freq[3]
	print q('O','O','O')
	print q('*','O','I-GENE')
	print e('endorphin','I-GENE')

initdict()
sentences = split_sentences(testdata)

for s in sentences:
	t=gettag(s)
	for i in range(len(s)):
		outfp.write(s[i]+" "+t[i]+'\n')
	outfp.write('\n')	

