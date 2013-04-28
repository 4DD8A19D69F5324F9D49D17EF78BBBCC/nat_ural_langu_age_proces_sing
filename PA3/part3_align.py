align_data = open('test.out').readlines()
ralign_data = open('test.rout').readlines()

kmax = int(align_data[-1].split(' ')[0])

align_list = []
ralign_list = []


for i in range(kmax):
    align_list.append([])
    ralign_list.append([])

for line in align_data:
    l = line.replace('\n', '').split(' ')
    idx = int(l[0]) - 1
    align_list[idx].append((int(l[1]), int(l[2])))

for line in ralign_data:
    l = line.replace('\n', '').split(' ')
    idx = int(l[0]) - 1
    ralign_list[idx].append((int(l[2]), int(l[1])))
    
def build_align_dict(align, ralign):
    ret = {}
    def upd(dic, key, val):
        if key not in dic:
            dic[key] = val
        else:
            dic[key] += val
    for key in align:
        upd(ret, key, 1)
    for key in ralign:
        upd(ret, key, 1)
    return ret

for k in range(kmax):
    dic = build_align_dict(align_list[k], ralign_list[k])
    outdic = {}
    visl = [0] * 100
    visr = [0] * 100
    for key in dic:
        if dic[key] == 2:
            outdic[key] = 1
            visl[key[0]] = 1
            visr[key[1]] = 1

    def dist(item, dic):
        ret = 10000
        for key in dic:
            ret = min(ret, abs(key[0] - item[0]) + abs(key[1] - item[1]))
        return ret
    

    flag = 1
    while flag:
        flag = 0
        mindis = 10000
        toadd = (0,0)
        for key in dic:
            if key not in outdic and (visl[key[0]] == 0 and visr[key[1]] == 0):
                flag = 1
                if dist(key,outdic)<mindis:
                    mindis=dist(key,outdic)
                    toadd=key
        if flag:
            outdic[toadd]=1
            visl[toadd[0]]=1
            visr[toadd[1]]=1
     
    for key in outdic:
        print k + 1, key[0], key[1]
    
        
    
    
    
    
