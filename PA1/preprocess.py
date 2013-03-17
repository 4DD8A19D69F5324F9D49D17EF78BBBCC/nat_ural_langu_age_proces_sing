import sys

fp = open("gene.origcount")
lines = fp.readlines()
rares = {}
for line in lines:
	l=line.replace('\n','').split(' ')
	if l[1]=="WORDTAG":
		count=int(l[0])
		tag=l[2]
		word=l[3]
		if count<5:
			rares[(tag,word)]=count
fp.close()

if len(sys.argv)!=3:
	print "Wrong Paratemers"
	quit()

src = open(sys.argv[1])
dest = open(sys.argv[2],'w')

lines = src.readlines()
for line in lines:
	l=line.replace('\n','').split(' ')
	if len(l)!=2:
		dest.write('\n')
		continue
	word=l[0]
	tag=l[1]
	if rares.has_key((tag,word)):
		word="_RARE_"
	dest.write(word+' '+tag+'\n')


