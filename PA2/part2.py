import json
from math import log

train = open('cfg.counts.new').readlines()
count = {}
wordcount = {}
follow = {}
follow_word = {}
rules = []
inf = -1e9

for line in train:
    def inc(dic, key, val):
        if key not in dic:
            dic[key] = val
        else:
            dic[key] += val
    def ap(dic, key, val):
        if key not in dic:
            dic[key] = [val]
        else:
            dic[key].append(val)
    l = line.replace('\n', '').split()
    if l[1] == 'NONTERMINAL':
        inc(count, l[2], int(l[0]))
    elif l[1] == 'UNARYRULE':
        inc(count, (l[3], l[2]), int(l[0]))
        inc(count, l[3], int(l[0]))
        ap(follow_word, l[3], l[2])
    elif l[1] == 'BINARYRULE':
        inc(count, (l[2], l[3], l[4]), int(l[0]))
        inc(count, l[2], int(l[0]))
        ap(follow, l[2], (l[3], l[4]))
        rules.append((l[2], l[3], l[4]))

def q(*tup):
    if tup in count and tup[0] in count:         
        return log(count[tup] * 1.00 / count[tup[0]])
    else:
        return inf


def parse(sentence): 
    dp = {}
    pre = {}
    s = sentence.replace('\n', '').split()
    def preprocess(word):
        if word not in count:
            return '_RARE_'
        else:
            return word
    ss = map(preprocess, s)
    for i in range(0, len(s)):
        for key in follow_word[ss[i]]:
            dp[(i, i, key)] = q(ss[i], key)
    def getdp(*cur):
        i = cur[0]
        j = cur[1]
        if (cur) in dp:
            return dp[(cur)]
        elif i==j:
            return inf
        else:
            if cur[2] not in follow:
                return inf
            dp[(cur)]=inf;
            for k in range(i, j):
                for nx in follow[cur[2]]:   
                    tmp = getdp(i, k, nx[0]) + getdp(k + 1, j, nx[1]) + q(cur[2],nx[0],nx[1])
                    if tmp>dp[(cur)]:
                        dp[(cur)]=tmp;
                        pre[(cur)]=((i,k,nx[0]),(k+1,j,nx[1]))
                        
            return dp[(cur)]    
        
                    
    fin_stat = (0, len(s) - 1, 'SBARQ')
    getdp(*fin_stat) 
    def get_tree(cur):
        if cur[0] == cur[1]:
            return [ cur[2], s[cur[0]] ]
        else:
            return [cur[2], get_tree(pre[cur][0]), get_tree(pre[cur][1])]
    return get_tree(fin_stat)


out = open('parse_test.out','w')
for line in open("parse_test.dat").readlines():
    tree= parse(line)
    out.write(json.dumps(tree)+"\n")
    print tree








        





    

