import re
import string
from collections import Counter

import numpy as np
from nltk.util import pad_sequence
from nltk.util import bigrams
from nltk.util import ngrams
from nltk.util import everygrams
from nltk.lm.preprocessing import pad_both_ends
from nltk.lm.preprocessing import flatten

def read_corpus(filename):
  with open(filename, "r",encoding="utf8") as file:
    lines = file.readlines()
    words = []
    for line in lines:
      words += re.findall(r'\w+', line.lower())

  return words

words = read_corpus("./data.csv")
print(f"There are {len(words)} total words in the corpus")

vocabs = set(words)
print(f"There are {len(vocabs)} unique words in the vocabulary")

word_counts = Counter(words)
print(word_counts["yêu"])

total_word_count = float(sum(word_counts.values()))
word_probas = {word: word_counts[word] / total_word_count for word in word_counts.keys()}

print(word_probas["yêu"])

def split(word):
  return [(word[:i], word[i:]) for i in range(len(word) + 1)]

def delete(word):
  return [l + r[1:] for l,r in split(word) if r]

def swap(word):
  return [l + r[1] + r[0] + r[2:] for l, r in split(word) if len(r)>1]

def replace(word):
  letters = string.ascii_lowercase
  return [l + c + r[1:] for l, r in split(word) if r for c in letters]

def insert(word):
  letters = string.ascii_lowercase
  return [l + c + r for l, r in split(word) for c in letters]

def edit1(word):
  return set(delete(word) + swap(word) + replace(word) + insert(word))

def edit2(word):
  return set(e2 for e1 in edit1(word) for e2 in edit1(e1))





def correct_spelling(word, vocabulary, word_probabilities):
  if word in vocabulary:
    print(f"{word} is already correctly spelt")
    return

  suggestions = edit1(word) or edit2(word) or [word]
  best_guesses = [w for w in suggestions if w in vocabulary]
  return [(w, word_probabilities[w]) for w in best_guesses]


word = "chnug"
corrections = correct_spelling(word, vocabs, word_probas)

if corrections:
  print(corrections)
  probs = np.array([c[1] for c in corrections])
  best_ix = np.argmax(probs)
  correct = corrections[best_ix][0]
  print(f"{correct} is suggested for {word}")

class SpellChecker(object):

  def __init__(self, corpus_file_path):
    with open(corpus_file_path, "r",encoding="utf8") as file:
      lines = file.readlines()
      words = []
      for line in lines:
        words += re.findall(r'\w+', line.lower())

    self.vocabs = set(words)
    self.word_counts = Counter(words)
    total_words = float(sum(self.word_counts.values()))
    self.word_probas = {word: self.word_counts[word] / total_words for word in self.vocabs}

  def _level_one_edits(self, word):
    letters = string.ascii_lowercase
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [l + r[1:] for l,r in splits if r]
    swaps = [l + r[1] + r[0] + r[2:] for l, r in splits if len(r)>1]
    replaces = [l + c + r[1:] for l, r in splits if r for c in letters]
    inserts = [l + c + r for l, r in splits for c in letters]

    return set(deletes + swaps + replaces + inserts)

  def _level_two_edits(self, word):
    return set(e2 for e1 in self._level_one_edits(word) for e2 in self._level_one_edits(e1))

  def check(self, word):
    candidates = self._level_one_edits(word) or self._level_two_edits(word) or [word]
    valid_candidates = [w for w in candidates if w in self.vocabs]
    return sorted([(c, self.word_probas[c]) for c in valid_candidates], key=lambda tup: tup[1], reverse=True)


checker = SpellChecker("./data.csv")


#Bi-gram

textdata_biGram = open("data.csv", "r",encoding="utf8").read()
class N_Gram:
  def __init__(self, word, probability):
    self.word = word
    self.probability = probability




def count(str1, str2):
    c = 0
    for i in str1:
        if re.search(i, str2):
            c = c + 1
    return c
# tim tu dung
def search_Word (data,word,wrong_words) :
    length_Of_wrong_word = len(wrong_words)
    bigram_word = []
    number_of_duplicate_character_max = 0;

    w1_max = 0
    solution_word = ""
    for i in range(len(data)) :

        if (data[i] == word) :
            one_bigram_word = data[i] +' ' + data[i+1]
            w1 = textdata_biGram.count(one_bigram_word)
            w2 = word_counts[data[i]]

            number_of_duplicate_character = count(wrong_words, data[i + 1])

            #chuan hoa du lieu
            if (w1 == 0) :
                w1 = 1
            length_word1 = len(data[i + 1])
            biGramp = N_Gram(data[i + 1], w1 / w2)
            bigram_word.append(biGramp)
            # du doan theo so ki tu giong nhau
            if (number_of_duplicate_character > number_of_duplicate_character_max) :
                if ((length_word1 - length_Of_wrong_word >= -1) and (length_word1 - length_Of_wrong_word <= 1)):
                    w1_max = w1
                    solution_word = data[i + 1]
                    number_of_duplicate_character_max = number_of_duplicate_character

                    #biGramp = N_Gram(data[i+1], w1 / w2)
                    #bigram_word.append(biGramp)

            #neu so ki tu bang nhau thi se du doan theo xac xuat
            if (number_of_duplicate_character == number_of_duplicate_character_max) :
                #biGram = N_Gram(data[i+1] , w1/w2)
                #bigram_word.append(biGram)

                #tu du doan phai co do dai lon, be hon so v tu dung la 1
                if( ( length_word1 - length_Of_wrong_word >= -1) and (length_word1 - length_Of_wrong_word <= 1) ):
                    if (w1 > w1_max):
                        solution_word = data[i + 1]
                        number_of_duplicate_character_max = number_of_duplicate_character
                        w1_max = w1

    result = sorted(bigram_word,key=lambda x: x.probability, reverse=True)

    for i in range(len(result)):
        print("( " + result[i].word + ", " + str(result[i].probability) + " )")
    print("Sửa từ: " + wrong_words + " trong " + word + " " + wrong_words + " là : " + word +" " +  solution_word)


#Test # hoa huệ, kiến trúc , kiến thức
previous_word = "kiến"
true_word = "trúc"
false_word = "tqúcd"

print(checker.check(false_word))
word_errorl_model = ""
if (len(checker.check(false_word)) > 0):
    word_errorl_model = checker.check(false_word)[0][0]
    print("Từ học theo errol model : " + word_errorl_model)
if not (word_errorl_model == true_word):
    search_Word(words,previous_word,false_word)

