corpus_en = open('corpus.en').readlines()
corpus_es = open('corpus.es').readlines()

c = {}
t = {}
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
        for i in xrange(len(es[k])):
            tmp.append([initial_t_value] * len(en[k]))
        delta.append(tmp)

def output():
    out = open("prob.part1", 'w')
    for key in t:
        if len(key) == 1:
            out.write("1 " + key + " " + str(t[key]) + "\n")
        else:
            out.write("2 " + key[0] + " " + key[1] + " " + str(t[key]) + "\n")

def update_c():
    for k in xrange(len(en)):
        if k % 100 == 0:
            print k
        for i, f in enumerate(es[k]):
            for j, e in enumerate(en[k]):
                def upd(dic, key, val):
                    if key not in dic:
                        dic[key] = val
                    else:
                        dic[key] += val
                upd(c, (e, f), delta[k][i][j])
                upd(c, e, delta[k][i][j])

def update_t():
    for k in xrange(len(en)):
        for f in es[k]:
            for e in en[k]:
                t[(f, e)] = c[(e, f)] / c[e]

def update_delta():
    for k in xrange(len(en)):
        for i, f in enumerate(es[k]):
            sum_prob = 0
            for j, e in enumerate(en[k]):
                sum_prob += t[(f, e)]
            for j, e in enumerate(en[k]):
                delta[k][i][j] = t[(f, e)] / sum_prob

def iter_one():
    update_c()
    update_t()
    update_delta()

if __name__ == '__main__':
    init()
    for i in range(5):
        print "iter ", i
        iter_one()
    output()



