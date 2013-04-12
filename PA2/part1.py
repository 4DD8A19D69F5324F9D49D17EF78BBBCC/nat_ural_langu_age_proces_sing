import json

count= {}
trees = open('parse_train.dat').readlines()


def get_count(tree):
    if len(tree)==2:
        if tree[1] not in count:
            count[tree[1]]=1;
        else:
            count[tree[1]]+=1;
    else:
        get_count(tree[1])
        get_count(tree[2])


def process(tree):
    if len(tree) == 2  and count[tree[1]]<5:
        tree[1] = '_RARE_'
    elif len(tree) == 3:
        process(tree[1])
        process(tree[2])
        


out=open("parse_train.dat.new",'w')

for treestr in trees:
    tree = json.loads(treestr)
    get_count(tree)


for treestr in trees:
    tree = json.loads(treestr)
    process(tree)
    out.write(json.dumps(tree)+'\n')
    


    


    






