#!/usr/bin/python3
# -*- coding: utf-8 -*-


##
# input parameters:
#       argv[1] = word
#       argv[2] = num_cores
#
##

# dependencies
import math, os, re, sys, json, time
import multiprocessing
import matplotlib.pyplot as plt
from joblib import Parallel, delayed

dfilepath = '../data/congressional-debates/dates.csv'
corpuspath =  '../data/congressional-globe/'
dictionary = []
with open ("../data/words.txt", "r") as d:
    for line in d:
        dictionary.append(line.rstrip().lower())
stoplist = "a about above after again against all am an and any are aren't as at be because been before being below between both but by can't cannot could couldn't did didn't do does doesn't doing don't down during each few for from further had hadn't has hasn't have haven't having he he'd he'll he's her here here's hers herself him himself his how how's i i'd i'll i'm i've if in into is isn't it it's its itself let's me more most mustn't my myself no nor not of off on once only or other ought our ours ourselves out over own same shan't she she'd she'll she's should shouldn't so some such than that that's the their theirs them themselves then there there's these they they'd they'll they're they've this those through to too under until up very was wasn't we we'd we'll we're we've were weren't what what's when when's where where's which while who who's whom why why's with won't would wouldn't you you'd you'll you're you've your yours yourself yourselves".split()

# given directory get the sentences that contain the searchword
def get_clean_sentences (dirname, fname, searchword):
    print ("getting sentences")
    words = []
    sentences = []
    ngram = []

    with open(dirname + "/" + fname, "r") as ifile:
        lines = []
        for  line in ifile:
            tokens = line.rstrip().split(" ")
            for t in tokens:
                t = re.sub("[^a-zA-Z]+", "", t).lower()
                if len(t) < 2:
                    continue
                if stoplist.count(t) == 0 and dictionary.count(t) > 0:
                    words.append(t)

    c = 0
    for w in words:
        if c < 10:
            ngram.append(w)
            c = c + 1
        else:
            sentences.append(ngram)
            ngram = []
            c = 0
    print ("done getting sentences")
    return sentences


# given session id return the date 
def get_date (sessionid):
    datefile = '../data/congressional-globe/dates.csv'
    with open(datefile, "r") as f:
        for line in f:
            if line[0] != '#':
                tokens = line.rstrip().split(',')
                if tokens[0] == sessionid:
                    date = tokens[1]
                    return date

def calc_sentiment (sentences):
    print ("getting sentiment")
    date = cg_get_date(dirname.split('/')[-2] + "_" + dirname.split('/')[-1])
    sentiments = []
    for s in sentences:
        sentiment = 5
        sentiments.append(sentiment)

    print("done getting sentiment")
    return date, sentiment

def get_dirnames ():
    path = '../data/congressional-globe/'
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

def main():
    word = sys.argv[1]
    cores = sys.argv[2]

    dirs = get_dirnames()
    for d in dirs:
        print ("processing dir ", d)
        s = get_clean_sentences(d, "all.txt", word)
        print (len(s))


if __name__ == "__main__":
    main()
