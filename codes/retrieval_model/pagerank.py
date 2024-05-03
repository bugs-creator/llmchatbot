import collections
graph={'node_name':('aim1','aim2')}

def pagerank(graph,d=0.85,init_score=1,it=25):
    node_score={}
    for node in graph:
        node_score[node]=init_score


    results=[]
    results.append(node_score.copy())
    for i in range(it):
        new_score=collections.defaultdict(int)
        for node in graph:
            score=node_score[node]/graph[node].__len__()
            for aim in graph[node]:
                new_score[aim]+=d*score
        for node in graph:
            new_score[node]+=(1-d)
        node_score=new_score
        results.append(dict(node_score.copy()))
    return results

lst=(["A","B","C"],["D","E","F"])





# g={"A":("B","C"),"B":("C"),"C":("A"),"D":("C")}