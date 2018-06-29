#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import os
from joblib import Parallel, delayed

def load_dictionary():
    dictionary = []
    with open ("words.txt", "r") as d:
        for line in d:
            dictionary.append(line.rstrip().lower())
    return dictionary

def load_stopwords():
    stopwords = []
    with open ("stop_words.txt", "r") as s:
        doc = s.read()
        stopwords = doc.rstrip().split(" ")
    return stopwords

def get_dirnames():
    path = '../../data/congressional-globe/raw-ocr-text/'
    sessions = []
    dirnames = []
    for i in range (23, 43): #for each Congress
        for dirname, subdirlist, filelist in os.walk(path + str(i)):
            dirnames.append(dirname)

    dirnames.sort()
    directories = []

    for dirname in dirnames:
       if "session" in dirname and os.listdir(dirname):
          directories.append(dirname)
    return directories

def clean_text(inputfile, dictionary, stopwords):
    print ("cleaning ", inputfile)
    words = []
    nlines = 0
    c = 0
    ifile = open(inputfile, "r")
    for l in ifile:
        nlines = nlines + 1

    ifile = open(inputfile, "r")
    for line in ifile:
        if c % 500 == 0:
            print ("cleaning ... " , "{0:.2f}".format(c/nlines * 100), " % done")
        tokens = line.rstrip().split(" ")
        for t in tokens:
            t = re.sub("[^a-zA-Z]+", "", t).lower()
            if len(t) < 2:
                continue
            if stopwords.count(t) == 0 and dictionary.count(t) > 0:
                words.append(t)
        c = c + 1


    return words

def create_ngrams(outputfile, words):
    print ("extracting ngrams and writing to ", outputfile)
    ngram = []
    ngrams = []
    
    counter = 0
    for i,w in enumerate(words):
        if i == len(w):
            ngrams.append(" ".join(ngram))

        if counter < 10:
            ngram.append(w)
            counter = counter + 1
        else:
            ngrams.append(" ".join(ngram))
            ngram = []
            counter = 0

    with open(outputfile, "w") as ofile:
        for n in ngrams:
            print(n, file=ofile)

def clean_and_write (directory, dictionary, stopwords):
    inputfile = directory + "/all.txt"
    outputfile = "../../data/congressional-globe/clean-text/" + directory.split('/')[-2] + "_" + directory.split('/')[-1] + ".txt"
    words = clean_text(inputfile, dictionary, stopwords)
    create_ngrams(outputfile, words)

def main():

    num_cores = 3

    dictionary = load_dictionary()
    stopwords = load_stopwords()

    dirs = get_dirnames()
    Parallel(n_jobs=num_cores)(delayed(clean_and_write)(d, dictionary, stopwords) for d in dirs)

if __name__ == "__main__":
    main()
