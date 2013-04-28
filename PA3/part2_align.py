
prob = open('prob.part2').readlines()
q = open('q.part2').readlines()
dic = {}
qdic = {}

prob_len = len(prob)
for i, line in enumerate(prob):
    if i % 10000 == 0:
        print 'initializing ', i, '/', prob_len
    l = line.replace('\n', '').split(' ')
    if int(l[0]) == 2:
        dic[(l[1], l[2])] = float(l[3])
    else:
        dic[l[1]] = float(l[2])


q_len = len(q)
for i, line in enumerate(q):
    if i % 10000 == 0:
        print 'loading Q data ', i, '/', q_len
    l = line.replace('\n', '').split(' ')
    a = int(l[0])
    b = int(l[1])
    c = int(l[2])
    d = int(l[3])
    e = float(l[4])
    qdic[(a, b, c, d)] = e
    


en_file = open('test.en').readlines()
es_file = open('test.es').readlines()
out_file = open('test.out', 'w')
en = [line.replace('\n', '').split(' ') for line in en_file]
es = [line.replace('\n', '').split(' ') for line in es_file]


for k in range(len(en)):
    align = [ 0 ] * (len(es[k]))
    prob = [0.0] * (len(es[k]))
    l = len(en[k])
    m = len(es[k])
    for i, es_word in enumerate(es[k]):
        for j, en_word in enumerate(en[k]):
            if (es_word, en_word) in dic and dic[(es_word, en_word)] * qdic[(j, i, l, m)] > prob[i]:
                prob[i] = dic[(es_word, en_word)] * qdic[(j, i, l, m)]
                align[i] = j
    for i in range(len(align)):
        out_file.write(str(k + 1) + " " + str(align[i] + 1) + " " + str(i + 1) + '\n')


