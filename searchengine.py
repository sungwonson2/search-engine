import json
import os
import time
import collections
import nltk
nltk.download('punkt')
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

#from sklearn.metrics.pairwise import cosine_similarity

ps = PorterStemmer()

from bs4 import BeautifulSoup
import tkinter as tk

def findTfIdf(tf, n, df):
    return (1 + log(tf,(2))) * log((n/df),(2))

class searchGUI(tk.Frame):
    def __init__(self, master):
        self.mainPage(master)

    def mainPage(self, master):
        self.empty = tk.Label(master, text = "")
        self.empty.grid(row=0, column = 0)
        self.label = tk.Label(master, text="What would you like to search for!")
        self.entry = tk.Entry(master)
        self.label.grid(row=10, column=1)
        self.entry.grid(row=11, column=1)
        self.button = tk.Button(master, text="Search", command = lambda: self.search(self.entry.get().lower(), master))
        self.button.grid(row=12, column = 1)
        self.label1 = tk.Label(master, text="")
        self.label2 = tk.Label(master, text="")
        self.label3 = tk.Label(master, text="")
        self.label4 = tk.Label(master, text="")
        self.label5 = tk.Label(master, text="")
        self.label6 = tk.Label(master, text="")
        self.label1.grid(row=13, column = 1)
        self.label2.grid(row=14, column = 1)
        self.label3.grid(row=15, column = 1)
        self.label4.grid(row=16, column = 1)
        self.label5.grid(row=17, column = 1)
        self.label6.grid(row=18, column = 1)

    def resultsPage(self, results, master):

        self.label1['text'] = (results[0])
        self.label2['text'] = (results[1])
        self.label3['text'] = (results[2])
        self.label4['text'] = (results[3])
        self.label5['text'] = (results[4])
        self.label6['text'] = (results[5])
        self.button = tk.Button(master, text="Search", command = lambda: self.mainPage(master))
        

# dot product: ((tf idf of word ^ 2 / length for every word) / (sqrt((tf idf of word) / length) ^ 2 for every word)) * (


    def search(self, token, master):
        results = []
        start = time.perf_counter()
        searchTerm = token.split()
        length = len(searchTerm)
        search = {}
        term = ps.stem(searchTerm[0])
        offset = 0
        with open('seek_dict' + term[0] + '.json') as seek_dict_file:
            data = json.loads(seek_dict_file.read())
            try:
                offset = data[term]
            except:
                pass
        #print(offset)
        with open('index' + term[0] + '.json') as json_file:
            json_file.seek(offset)
            json_file.readline()
            json_file.readline()
            output = {}
            current = ""
            current = json_file.readline()
            counter = 0
            while '}' not in current:
                #print(current)
                counter += 1
                current = current.strip().split()
                output[current[0].strip(":\"")] = float(current[1].strip(','))
                current = json_file.readline()
            for url in output:
                if url in search:
                    search[url] += output[url]
                else:
                    search[url] = output[url]
        for i in range(len(searchTerm) - 1):
            delete = []
            with open('seek_dict' + term[0] + '.json') as seek_dict_file:
                data = json.loads(seek_dict_file.read())
                try:
                    offset = data[term]
                except:
                    pass
            with open('index' + term[0] + '.json') as json_file:
                json_file.seek(offset)
                json_file.readline()
                json_file.readline()
                output = {}
                current = ""
                current = json_file.readline()
                while '}' not in current:
                    current = current.strip().split()
                    output[current[0].strip(":\"")] = float(current[1].strip(','))
                    current = json_file.readline()
                for url in search:
                    if url in output:
                        search[url] += output[url]
                    else:
                        delete.append(url)
                for deleted in delete:
                    del search[deleted]
        search = collections.Counter(search)
        highest = search.most_common(5)
        left = 5 - len(highest)
        for i in highest:
            results.append(str(i[0]))
        if left > 0:
            for i in range(left):
                results.append("url not available")
        results.append("Time: " + str(time.perf_counter() - start))
        self.resultsPage(results, master)

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("1000x500") 
    window = searchGUI(root)
    root.mainloop()
