import os
import time

import utils
from utils import tokenize
import argparse

try:
    from tqdm import tqdm
except:
    tqdm = lambda x: x

DOCUMENT_PATH = 'data/documents'


def indexing(path, type="small"):
    """
    Indexing documents and summon corpus
    :param path: documents dir path
    :param type: corpus type. It can be "large" or "small"
    :return: inverted index map, BM25 value map, documents, average document length, documents count
    """
    file_dict = {}
    documents = {}

    def read(file_path, encoding=None):
        with open(file_path, encoding=encoding) as file:
            content = file.read()
            file_dict[file_name] = tokenize(content, handle=False)

    print("reading documents...")

    if type == "small":
        for file_name in tqdm(os.listdir(path)):
            file_path = os.path.join(path, file_name)
            read(file_path)
    elif type == "large":
        for _dir in tqdm(os.listdir(path)):
            _dir = os.path.join(path, _dir)
            if os.path.isdir(_dir):
                for file_name in os.listdir(_dir):
                    file_path = os.path.join(_dir, file_name)
                    read(file_path, encoding="utf-8")

    reversed_map_raw = {}

    print("counting words frequency...")

    for file in tqdm(file_dict):
        for word in file_dict[file]:
            f = reversed_map_raw.get(word, {})
            reversed_map_raw[word] = f
            reversed_map_raw[word][file] = file_dict[file][word]

    inverted_map = {}

    total_length = 0

    print("tokenizing...")
    for word in tqdm(reversed_map_raw):
        _word = utils.STEMMER.stem(word)
        if _word in utils.STOP_WORDS:
            continue
        dic = inverted_map.get(_word, {})
        for file in reversed_map_raw[word]:
            count = dic.get(file, 0)
            length = reversed_map_raw[word][file]
            dic[file] = count + length

            document = documents.get(file, {})
            document_length = document.get('length', 0)
            document_length += length
            total_length += length
            document['length'] = document_length
            documents[file] = document
        inverted_map[_word] = dic

    documents_count = documents.__len__()
    average_length = total_length / documents_count

    value_map = {}

    print('computing values...')
    for word in tqdm(inverted_map):
        value_item = value_map[word] = {}
        file_list = inverted_map[word]
        for file in file_list:
            value = utils.BM25Step(file_list[file], documents[file]['length'], average_length, documents_count,
                                   file_list.__len__())
            value_item[file] = value

    return inverted_map, value_map, documents, average_length, documents_count


if __name__ == '__main__':
    start=time.time()
    parser = argparse.ArgumentParser('preprocess')
    parser.add_argument('-p', '--path', type=str, default=DOCUMENT_PATH,
                        help='document path')
    parser.add_argument('-t', '--type', type=str, default="small",
                        help='large or small')

    args = parser.parse_args().__dict__
    if args['type'] == 'large':
        index = indexing(args['path'], type="large")
    elif args['type'] == 'small':
        index = indexing(args['path'], type="small")
    else:
        raise Exception("No such type!!!")

    document_index = {}
    total_length = 0

    corpus = {}
    corpus["value_map"] = index[1]

    print('saving...')
    utils.saveJSON(corpus)
    print('complete!    time cost: ',time.time()-start)
