import re
from nltk.util import ngrams
import numpy as np
import pandas as pd


from nltk.corpus import reuters
from nltk import bigrams, trigrams
from collections import Counter, defaultdict

text = [['a', 'b', 'c'], ['a', 'c', 'd', 'c', 'e', 'f']]

from nltk.util import pad_sequence
list(pad_sequence(text[0],
                  pad_left=True, left_pad_symbol="<s>",
                  pad_right=True, right_pad_symbol="</s>",
                  n=2))

padded_sent = list(pad_sequence(text[0], pad_left=True, left_pad_symbol="<s>",
                                pad_right=True, right_pad_symbol="</s>", n=2))
print(list(ngrams(padded_sent, n=2)))

textdata = open("data.csv", "r",encoding="utf8").read()

def read_corpus(filename):
  with open(filename, "r",encoding="utf8") as file:
    lines = file.readlines()
    words = []
    for line in lines:
      words += re.findall(r'\w+', line.lower())

  return words

words = read_corpus("./data.csv")
word_counts = Counter(words)
print(textdata.count("hoa quả"))

print(word_counts["hoa"])
print(word_counts["quả"])
# p = p(w(i-1) w(i)) / p(wi-1)
def bi_grams (a,b) :
    p = textdata.count(a) / word_counts[b]
    return p

#p(quả | hoa)
print(bi_grams("hoa học", "hoa"))

def ramdom_Ngram (a):
    for a in words :
        index = words.index(a)
        print(words[index-1])
    return 0

def search_Word (data,word) :
    bigram_word = {}
    w1_max = 0
    solution_word = ""
    for i in range(len(data)) :

        if (data[i] == word) :
            one_bigram_word = data[i] +' ' + data[i+1]
            w1 = textdata.count(one_bigram_word)
            w2 = word_counts[data[i]]
            if(w1 > w1_max ):
                w1_max = w1
                solution_word = data[i+1]
                print(w1_max)
                print(solution_word)
    print(solution_word)




search_Word(words,"hoa")


