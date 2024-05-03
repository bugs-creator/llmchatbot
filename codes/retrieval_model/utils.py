import collections
import json
import re
import porter
import math
import os
import sys

directory=sys.argv[0][:-10]
f = open(os.path.join(directory,"stopwords.txt"))

STEMMER = porter.PorterStemmer()
STOP_WORDS = set(f.read().split('\n'))


def BM25Step(frequency, document_length, average_length, total_document_count, contain_document_count, k=1, b=0.75):
    """
    Compute one part of BM25 score
    :param frequency: frequency of words
    :param document_length: document length
    :param average_length: average length
    :param total_document_count: total count
    :param contain_document_count: contain count
    :param k: constant
    :param b: constant
    :return: score
    """
    s1 = k * ((1 - b) + (b * document_length) / average_length)
    part1 = math.log2((total_document_count - contain_document_count + 0.5)
                      / (contain_document_count + 0.5))

    part2 = frequency * (k + 1)

    part3 = (frequency + s1)

    return part1 * part2 / part3


def tokenize(document: str, handle=True):
    """
    convert document to word frequency list
    :param document: document in string
    :param handle: stem and remove stop word
    :return: word frequency list
    """
    document = document.lower()
    match_pattern = re.findall(r'\b[a-z]{3,15}\b', document)
    frequency = {}
    for word in match_pattern:
        count = frequency.get(word, 0)
        if handle:
            word = STEMMER.stem(word)
            if word in STOP_WORDS:
                continue
        frequency[word] = count + 1
    return frequency


def readJSON(path='corpus.json'):
    """
    read json file to dict
    :param path: file path
    :return: dict
    """
    with open(path) as f:
        return json.load(f)


def saveJSON(dict, path='corpus.json'):
    """
    save dict to json file
    :param dict: saving dict
    :param path: saving path
    """
    with open(path, "wb") as f:
        j = json.dumps(dict)
        f.write(j.encode('utf-8'))
        f.close()


def readEvaluation(path):
    """
    read evaluation queries and qrels
    :param path: dir path
    :return: queries and label
    """
    queries = os.path.join(path, "queries.txt")
    qrels = os.path.join(path, "qrels.txt")
    q = {}
    label = collections.defaultdict(list)

    with open(queries, encoding='utf-8') as f:
        content = f.read().split('\n')
        for i in content:
            i = i.split(' ', 1)
            if i.__len__() != 2:
                break
            q[i[0]] = i[1]

    with open(qrels, encoding='utf-8') as f:
        content = f.read().split('\n')
        for i in content:
            i = i.split(' ')
            i = [x.strip() for x in i if x.strip() != '']
            if i.__len__() < 4:
                break
            label[i[0]] += [(i[2], i[3])]
    return q, dict(label)
