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
# tinh toan bi _gram
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

# ham tim so ki tu giong nhau giua tu du doan va tu sai
def count(str1, str2):
    c = 0
    for i in str1:
        if re.search(i, str2):
            c = c + 1
    return c
# tim tu dung
def search_Word (data,word,wrong_words) :
    bigram_word = {}
    number_of_duplicate_character_max = 0;

    w1_max = 0
    solution_word = ""
    for i in range(len(data)) :

        if (data[i] == word) :
            one_bigram_word = data[i] +' ' + data[i+1]
            w1 = textdata.count(one_bigram_word)
            w2 = word_counts[data[i]]

            number_of_duplicate_character = count(wrong_words, data[i + 1])
            # du doan theo so ki tu giong nhau
            if (number_of_duplicate_character > number_of_duplicate_character_max) :
                w1_max = w1
                solution_word = data[i + 1]
                number_of_duplicate_character_max = number_of_duplicate_character

            #neu so ki tu bang nhau thi se du doan theo xac xuat
            if (number_of_duplicate_character == number_of_duplicate_character_max) :
                if(w1 > w1_max) :
                    solution_word = data[i+1]
                    number_of_duplicate_character_max = number_of_duplicate_character
                    w1_max = w1




    print("Từ tốt nhất sau từ  " + word + " là :" + solution_word)




search_Word(words,"kinh","deahn")


