import argparse
import os
import time

import evaluation
from utils import readJSON
from ir_system import search
import utils

import json

try:
    from tqdm import tqdm
except:
    tqdm = lambda x: x

if __name__ == '__main__':
    # initialize parser
    parser = argparse.ArgumentParser('search')
    parser.add_argument('-m', '--method', type=str, default="manual",
                        help='choose method')
    parser.add_argument('-p', '--path', type=str, default="data",
                        help='choose qrels file path')
    parser.add_argument('-t', '--type', type=str, default="small",
                        help='large or small')
    parser.add_argument('-c', '--corpus', type=str, default=None,
                        help='choose corpus file path')
    parser.add_argument('-q', '--query', type=str, default="",
                        help='type query(only available if method is "api")')

    args = parser.parse_args().__dict__


    # if the corpus is none
    if args["corpus"]==None:
        # read corpus from path
        args["corpus"]=os.path.join(args["path"],"corpus.json")
    # construct corpus
    corpus = readJSON(args['corpus'])

    if args['method'] == "manual":
        query = input("Enter query: ")
        while query.lower() != 'quit':
            start = time.time()
            results = search(query, corpus=corpus)
            print("\nResults for query [{}]  time cost: {}".format(query, time.time() - start))
            [print("{} {} {}".format(i + 1, result[0], result[1])) for i, result in enumerate(results)]
            query = input("Enter query: ")
    # if mode is evaluation
    elif args['method'] == "evaluation":
        path = args.get('path')
        queries, y_label = utils.readEvaluation(os.path.join(path, 'files'))
        score = [0, 0, 0, 0, 0, 0, 0]
        start = time.time()
        unjudged = True
        output = ""
        if args['type'] == 'large':
            unjudged = True
        else:
            unjudged = False
        for i in tqdm(queries):
            y_pred = search(queries[i], corpus=corpus)
            for ii, r in enumerate(y_pred):
                output += "{} Q0 {} {} {} 19206206\n".format(i, r[0], ii + 1, r[1])
            result = evaluation.evaluation(y_pred, y_label[i], unjudged)
            for ii in range(7):
                score[ii] += result[ii]
        # print results
        print("\nTime cost:    ", time.time() - start, "\n")
        print("Evaluation results:")
        print("Precision:       ", score[0] / queries.__len__())
        print("Recall:          ", score[1] / queries.__len__())
        print("P@10:            ", score[2] / queries.__len__())
        print("R-precision:     ", score[3] / queries.__len__())
        print("MAP:             ", score[4] / queries.__len__())
        print("bpref:           ", score[5] / queries.__len__())
        print("NDCG:            ", score[6] / queries.__len__())

        print("\nsaving in output.txt...")
        # save output
        with open("output.txt", "wb") as f:
            f.write(output.encode("gbk"))
    # if using api
    elif args['method']=="api":
        query = args['query']
        start = time.time()
        results = search(query, corpus=corpus)
        # print("\nResults for query [{}]  time cost: {}".format(query, time.time() - start))

        print(json.dumps({"time":time.time()-start,"result":results}))
        # [print("{} {} {}".format(i + 1, result[0], result[1])) for i, result in enumerate(results)]

    # if not in given method, do nothing
    else:
        print("no such method")
