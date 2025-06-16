# Michael Rizig
# CS7263
# Professor Jiho Noh
# 6/3/25
# Vocabulary and Corpus Statistics
import os
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
class GenerateCorpusStatistics:

    def __init__(self,directory):
        self.unique_words_set = {}
        self.corpus = {}
        self.total_words = 0
        self.directory = directory
        self.process()
        self.print_statistics()
    # preprocess the scraped set of webpages
    def process(self):
        for filename in os.listdir(self.directory):
            # keep track if a word has appeared in this docu before
            frequency = {}
            with open(f"{self.directory}{filename}","r") as file:
                # read text and tokenize
                text = file.read()
                text = text.lower()
                text = word_tokenize(text)
                # store all unique words
                for word in text:
                    self.unique_words_set[word] = self.unique_words_set.get(word,0)+1
                # store total words in all articles (non-unique)
                self.total_words+=len(text)
                # store each words total count and document count
                for word in text:
                    add = 0 # if word has appeared in document before (if its in the freq dict) then dont incriment that words document count
                    if word not in frequency:
                        add = 1
                        frequency[word] = 1
                    # store each word as a tuple, setting the value to either (0,0) or what the value currently is +1 total count
                    # for docu count im just adding the 'add' var that alr determined if document count for that word should be incremented or not
                    self.corpus[word] = (self.corpus.get(word,(0,0))[0]+1 ,self.corpus.get(word,(0,0))[1]+add)

        # sort the dictionary by the total count value in each key value tuple (key, (total count, document count))
        self.sorted_dict = sorted(self.corpus.items(), key=lambda item: item[1])
        # remove punctuation
        self.sorted_dict = [t for t in self.sorted_dict if t[0] not in string.punctuation]
        # remove stopwords via nltk
        stopwordsset = set(stopwords.words('english'))
        self.sorted_dict_no_stopwords = [t for t in self.sorted_dict if t[0] not in stopwordsset]

        #print(sorted_dict)
    # print the statistics of the preprocessing
    def print_statistics(self):
            print("Total words: " , self.total_words)
            print("Total words (stopwords removed):", len(self.sorted_dict))
            print("Unique words: ", len(self.unique_words_set))
            print("Average Page Length: ", self.total_words/ len(os.listdir(self.directory)))
            # last 30 words are highest, so grabing last 30 words and reversing list
            top_30 = self.sorted_dict[-30:][::-1]
            print("Top 30 words (with stopwords): ")
            counter=1
            for x in top_30:
                print(f"\t{counter}: '{x[0]}' Count: {x[1][0]} Documents: {x[1][1]}")
                counter+=1
            top_30_nostop = [x for x in self.sorted_dict_no_stopwords[-30:]][::-1]
            print("Top 30 words: (without stopwords) ")
            counter=1
            for x in top_30_nostop:
                print(f"\t{counter}: '{x[0]}' Count: {x[1][0]} Documents: {x[1][1]}")
                counter+=1

GenerateCorpusStatistics("webpages/")
