import json
import os
import time
import collections
from math import log
import nltk
nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import math
from sys import getsizeof

ps = PorterStemmer()

from bs4 import BeautifulSoup

def findTfIdf(tf, n, df):
    return (1 + log(tf,(2))) * log((n/df),(2))

def index():
    start_time = time.time()
    entries = os.listdir('DEV')
    entryLen = len(entries)
    invertedIndex = {"a": {}, "b": {}, "c": {}, "d": {}, "e": {}, "f": {}, "g": {}, "h": {},
                     "i": {}, "j": {}, "k": {}, "l": {}, "m": {}, "n": {}, "o": {}, "p": {},
                     "q": {}, "r": {}, "s": {}, "t": {}, "u": {}, "v": {}, "w": {}, "x": {},
                     "y": {}, "z": {}, "1": {}, "2": {}, "3": {}, "4": {}, "5": {}, "6": {},
                     "7": {}, "8": {}, "9": {}, "0": {}
                     }
    weightMultiplier = {"title" : 10, "h1": 5, "h2": 5, "h3": 4, "h4": 4, "h5":3, "h6":2, "b":2}
    docId = 0
    dirCounter = 0
    keyCounter = 0

    #tf-idf = (1 + log(tf)) x log(N/df)
    #tf is number of occurences of i in j
    #tf is invertedIndex[word][docId]/sizes[docId]
    #df is number of documents containing i
    #df is len(invertedIndex[word])
    #N is total number of documents
    #N is len(invertedIndex)

    for url in entries:
        entries2 = os.listdir('DEV/' + url)
            
        for file in entries2:
            with open(os.path.join('DEV/',url,file)) as json_file:
                data = json.loads(json_file.read())
                output = data['content']
                specificUrl = data['url']
                if '#' not in specificUrl:
                    soup = BeautifulSoup(output, 'html.parser')
                    try:
                        contents = soup.get_text().split()
                        for token in contents:
                            token = token.lower()
                            token = ps.stem(token)
                            if len(token) > 1 and token.isalnum():
                                if token[0] in invertedIndex:
                                    if token in invertedIndex[token[0]].keys():
                                        if specificUrl in invertedIndex[token[0]][token].keys():
                                            invertedIndex[token[0]][token][specificUrl] += 1
                                        else:
                                            invertedIndex[token[0]][token][specificUrl] = 1
                                    else:
                                        invertedIndex[token[0]][token] = {specificUrl: 1}
                        for lines in soup.find_all(weightMultiplier):
                            for token in word_tokenize(lines.get_text()):
                                token = token.lower()
                                token = ps.stem(token)
                                if len(token) > 1 and token.isalnum():
                                    if token[0] in invertedIndex:
                                        if token in invertedIndex[token[0]].keys():
                                            if specificUrl in invertedIndex[token[0]][token].keys():
                                                invertedIndex[token[0]][token][specificUrl] += weightMultiplier[lines.name]
                                            else:
                                                invertedIndex[token[0]][token][specificUrl] = weightMultiplier[lines.name]
                                        else:
                                            invertedIndex[token[0]][token] = {specificUrl: weightMultiplier[lines.name]}
                    except UnicodeDecodeError:
                        print('error')
                json_file.close()
                docId += 1
        dirCounter += 1
    n = docId

    print("FiRST PART")
    
    for key in invertedIndex:
        keyCounter += len(invertedIndex[key])
        for token in invertedIndex[key]:
            for doc in invertedIndex[key][token]:
                invertedIndex[key][token][doc] = findTfIdf(invertedIndex[key][token][doc], n, len(invertedIndex[key][token]))
    popular_terms = {}
    for key in invertedIndex:
        seek_dict = {}
        #counter = 0
        with open('index' + key + '.json', 'w') as indexFile:
            for token in invertedIndex[key]:
                seek_dict[token] = indexFile.tell()
                temp = {token: invertedIndex[key][token]}
                json.dump(temp, indexFile, indent = 2)
            indexFile.close()
        with open('seek_dict' + key + '.json', 'w') as seekDictFile:
            json.dump(seek_dict, seekDictFile, indent = 2)
    keyCounter += len(invertedIndex.keys())
    with open('output2.txt', 'w') as outputFile:
        outputFile.write('token count: ' + str(len(invertedIndex.keys())))
        outputFile.write('\nnumber of docs: ' + str(docId - 1))
    outputFile.close()

    print('token count: ' + str(keyCounter))
    print('number of docs: ' + str(docId))
    print('finished')
        

if __name__ == '__main__':
    start_time = time.time()
    index()
    print(str(time.time() - start_time))
