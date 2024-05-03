from utils import tokenize,  BM25Step
import collections


def BM25(document_id, query_token, corpus, k=1, b=0.75):
    """
    Compute BM25 score
    :param document_id: document id in corpus
    :param query_token: tokenized query
    :param corpus: scope of search
    :param k: constant
    :param b: constant
    :return: BM25 score
    """
    score = 0
    document = corpus['document_index'][document_id]
    for token in query_token:
        if document_id not in corpus['inverted_list'][token]:
            continue
        score += BM25Step(corpus['inverted_list'][token][document_id],
                          document['length'], corpus['average_length'],
                          corpus['total_document'],
                          corpus['inverted_list'][token].__len__(),
                          k=k, b=b)

    return score


def search(query, corpus, limit=15):
    """
    Search documents in corpus
    :param query: query sentence
    :param corpus: search scope
    :param limit: how many relevant results will be returned
    :return: a list of relevant documents, the format is [(id, score),...]
    """
    query_token = tokenize(query)
    documents = collections.defaultdict(int)
    for token in query_token:
        file_list = corpus["value_map"].get(token, {})
        for file in file_list:
            documents[file] += file_list[file]

    documents = list(documents.items())
    documents.sort(key=lambda x: x[1], reverse=True)

    return documents[:limit]
