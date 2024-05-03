import math


def precision(y_pred, y_label):
    y_pred = set([i[0] for i in y_pred])
    y_label = list(filter(lambda x: x[1]!='0', y_label))
    y_label = set([i[0] for i in y_label])
    return y_pred.intersection(y_label).__len__() / y_pred.__len__()


def recall(y_pred, y_label):
    y_pred = set([i[0] for i in y_pred])
    y_label = list(filter(lambda x: x[1] != '0', y_label))
    y_label = set([i[0] for i in y_label])
    return y_pred.intersection(y_label).__len__() / y_label.__len__()


def pAtN(y_pred,y_label,n=10):
    return precision(y_pred[:n],y_label)


def R_precision(y_pred,y_label):
    y_label = list(filter(lambda x: x[1] != '0', y_label))
    return pAtN(y_pred,y_label,n=y_label.__len__())


def MAP(y_pred,y_label):
    y_pred = [i[0] for i in y_pred]
    y_label = list(filter(lambda x: x[1] != '0', y_label))
    y_label = [i[0] for i in y_label]
    count=0
    score=0
    for i,pred in enumerate(y_pred):
        if pred in y_label:
            count+=1
            score+=count/(i+1)
    return score/y_label.__len__()


y_pred=[("14",0.5),("12",0.5),("9",0.5),("3",0.5),("19",0.5),("4",0.5),("18",0.5),("17",0.5),("10",0.5),("1",0.5)]

y_label=[("1",'1'),("3",'1'),("7",'1'),("12",'1'),("14",'1'),("20",'1'),("2",'0'),("4",'0'),("6",'0'),("8",'0'),("20",'0')]

def bpref(y_pred,y_label,unjudged=True):
    if unjudged:
        y_pred = [i[0] for i in y_pred]
        y_relevant = list(filter(lambda x: x[1] != '0', y_label))
        y_relevant  = [i[0] for i in y_relevant ]
        y_nonRelevant=list(filter(lambda x: x[1] == '0', y_label))
        y_nonRelevant = [i[0] for i in y_nonRelevant ]
        R=y_relevant.__len__()
        score=0
        count=0
        for i in y_pred:
            if i in y_nonRelevant:
                count+=1
            elif i in y_relevant:
                score+=1-min(count,R)/R
        return score/R
    else:
        y_pred = [i[0] for i in y_pred]
        y_relevant = list(filter(lambda x: x[1] != '0', y_label))
        y_relevant  = [i[0] for i in y_relevant ]
        R=y_relevant.__len__()
        score=0
        count=0
        for i in y_pred:
            if i not in y_relevant:
                count+=1
            else:
                score+=1-min(count,R)/R
        return score/R

a=[(16,1),(14,1),(11,1),(6,1),(9,1)]
b=[(1,2),(5,3),(6,1),(8,1),(9,2),(11,3),(13,2),(15,1)]
def NDCG(y_pred,y_label):
    y_pred = [i[0] for i in y_pred]
    y_label = list(filter(lambda x: x[1] != '0', y_label))
    y_label=dict(y_label)

    def DCG(y_pred,y_label):
        score=0
        for i,document in enumerate(y_pred):
            if document in y_label:
                if i==0:
                    score+=float(y_label[document])
                    continue
                score += float(y_label[document])/math.log2(i+1)
        return score

    def IDCG(y_label, count=15):
        y_label = list(y_label.items())
        y_label.sort(key=lambda x: x[1], reverse=True)
        score = 0
        for i, document in enumerate(y_label):
            if i >= count:
                break
            if i == 0:
                score += float(document[1])
                continue
            score += float(document[1]) / math.log2(i + 1)
        return score

    return DCG(y_pred,y_label)/IDCG(y_label,count=y_pred.__len__())


def evaluation(y_pred,y_label,unjudged=True):
    return (precision(y_pred, y_label),
            recall(y_pred, y_label),
            pAtN(y_pred, y_label),
            R_precision(y_pred, y_label),
            MAP(y_pred, y_label),
            bpref(y_pred, y_label,unjudged=unjudged),
            NDCG(y_pred, y_label))



