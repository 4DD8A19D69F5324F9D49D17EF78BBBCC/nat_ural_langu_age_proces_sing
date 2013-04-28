corpus_en = open('corpus.en').readlines()
corpus_es = open('corpus.es').readlines()

c = {}
t = {}
q = {}
delta = []

en = [ line.replace('\n', '').split(' ') for line in corpus_en ]
es = [ line.replace('\n', '').split(' ') for line in corpus_es ]

en_words_count = 0
for line in en:
    en_words_count += len(line)

corpus_len = len(corpus_en)
num_iterations = 20
initial_t_value = 1.0 / en_words_count

def init():
    for k in xrange(len(en)):
        tmp = []
        l = len(en[k])
        m = len(es[k])
        for i in xrange(len(es[k])):
            tmp.append([initial_t_value] * len(en[k]))
            for j in xrange(len(en[k])):
                q[(j, i, l, m)] = 1.0 / (l + 1)
        delta.append(tmp)
    prob = open('prob.part1').readlines()
    prob_len = len(prob)
    
    for i, line in enumerate(prob):
        if i % 10000 == 0:
            print 'initializing ', i, '/', prob_len
        l = line.replace('\n', '').split(' ')
        if int(l[0]) == 2:
            t[(l[1], l[2])] = float(l[3])
    update_delta()


def output():
    out = open("prob.part2", 'w')
    for key in t:
        if len(key) == 2:
            out.write("2 " + key[0] + " " + key[1] + " " + str(t[key]) + "\n")
    out2 = open('q.part2', 'w')
    for key in q:
        out2.write(str(key[0]) + ' ' + str(key[1]) + ' ' + str(key[2]) + ' ' + str(key[3]) + ' ' + str(q[key])+'\n')

def update_c():
    for k in xrange(len(en)):
        if k % 100 == 0:
            print k
        l = len(en[k])
        m = len(es[k])
        for i, f in enumerate(es[k]):
            for j, e in enumerate(en[k]):
                def upd(dic, key, val):
                    if key not in dic:
                        dic[key] = val
                    else:
                        dic[key] += val
                upd(c, (e, f), delta[k][i][j])
                upd(c, e, delta[k][i][j])
                upd(c, (j, i, l, m) , delta[k][i][j])
                upd(c, (i, l, m), delta[k][i][j])

def update_t():
    for k in xrange(len(en)):
        for f in es[k]:
            for e in en[k]:
                t[(f, e)] = c[(e, f)] / c[e]
                
def update_q():
    for k in xrange(len(en)):
        l = len(en[k])
        m = len(es[k])
        for i in xrange(len(es[k])):
            for j in xrange(len(en[k])):
                q[(j, i, l, m)] = c[(j, i, l, m)] / c[(i, l, m)]

def update_delta():
    for k in xrange(len(en)):
        l = len(en[k])
        m = len(es[k]) 
        for i, f in enumerate(es[k]):
            sum_prob = 0
            for j, e in enumerate(en[k]):
                sum_prob += t[(f, e)] * q[(j, i, l, m)]
            for j, e in enumerate(en[k]):
                delta[k][i][j] = t[(f, e)] * q[(j, i, l, m)] / sum_prob

def iter_one():
    update_c()
    update_t()
    update_q()
    update_delta()

if __name__ == '__main__':
    init()
    for i in range(5):
        print "iter ", i
        iter_one()
    output()



