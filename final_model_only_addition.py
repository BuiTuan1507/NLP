import pymongo


s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'

def remove_accents(input_str):
	s = ''
	for c in input_str:
		if c in s1:
			s += s0[s1.index(c)]
		else:
			s += c
	return s

def check_spell(to_model_sentence):
    print("_____________________")
    print("câu trước khi sửa: ", to_model_sentence,)
    preword = 'preword'
    result = ""
    word_list = to_model_sentence.split(" ")
    word_list.append('afterword')
    for i in range(len(word_list)-1):
        word_re = check_spell_word(preword, word_list[i], word_list[i+1])
        result = result + " " + word_re
        preword = word_re
    print("câu sau khi sửa: ", result,)
    print("_____________________")
    return result

def edit_accents(str1, str2):
    return remove_accents(str1) == remove_accents(str2)


def editDistance(str1, str2, m, n):

    # If first string is empty, the only option is to
    # insert all characters of second string into first
    if m == 0:
        return n

    # If second string is empty, the only option is to
    # remove all characters of first string
    if n == 0:
        return m

    # If last characters of two strings are same, nothing
    # much to do. Ignore last characters and get count for
    # remaining strings.
    if str1[m - 1] == str2[n - 1]:
        return editDistance(str1, str2, m - 1, n - 1)

    # If last characters are not same, consider all three
    # operations on last character of first string, recursively
    # compute minimum cost for all three operations and take
    # minimum of three values.
    replace_value = 1
    if (edit_accents(str1[m - 1], str2[n - 1])):
        replace_value = 0.75

    return replace_value * 1 + min(editDistance(str1, str2, m, n - 1),  # Insert
                   editDistance(str1, str2, m - 1, n),  # Remove
                   editDistance(str1, str2, m - 1, n - 1)  # Replace
                   )
def edit_distance(str1, str2):
    return editDistance(str1, str2, len(str1), len(str2))

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Database
mydb = myclient["sua_loi_chinh_ta"]
print(myclient.list_database_names())

# Colection
bigramModel = mydb["bigram"]
print(mydb.list_collection_names())

# Error model
# Insert to colection
import re
import string
from collections import Counter

import numpy as np

def read_corpus(filename):
  with open(filename, "r",encoding="utf8") as file:
    lines = file.readlines()
    words = []
    for line in lines:
      words += re.findall(r'\w+', line.lower())
  return words

words = read_corpus("./Viet74K.txt")
print(f"There are {len(words)} total words in the corpus")
vocabs = set(words)
print(f"There are {len(vocabs)} unique words in the vocabulary")
word_counts = Counter(words)
total_word_count = float(sum(word_counts.values()))
word_probas = {word: word_counts[word] / total_word_count for word in word_counts.keys()}

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
    return
  suggestions = edit1(word) or edit2(word) or [word]
  best_guesses = [w for w in suggestions if w in vocabulary]
  return [(w, word_probabilities[w]) for w in best_guesses]

def get_pos_error(word):
  corrections = correct_spelling(word, vocabs, word_probas)
  pos_rs = []
  if corrections:
    for c in corrections:
      pos_rs.append({'w': c[0], 'p': c[1]})
  return {'word': word, 'pos': pos_rs}

#End error model



# Find by word

def find_pos(preword, word):
    error_pos = get_pos_error(word)['pos']
    if (preword == 'preword'):
        bigram_pos = find_first_words(vocabs, word)
        return error_pos, bigram_pos
    bigram_pos = []
    for rs in bigramModel.find({"word": preword}):
        if rs is not None:
            if (len(bigram_pos) == 0):
                bigram_pos.extend(rs['pos'])
            else:
                for r in rs['pos']:
                    flag = 0
                    for b in bigram_pos:
                        if r['w'] == b:
                            flag = 1
                            b['p'] = b['p'] + r['p']
                            break
                    if flag == 0:
                        bigram_pos.append(r)
    print(bigram_pos)
    return error_pos, bigram_pos

# Predict cau:
def find_word_array_bigram(pre_word):
    rs = bigramModel.find_one({"word": pre_word})
    bigram_vocab = []
    try:
        for b_v in rs['pos']:
            bigram_vocab.append(b_v)
        return bigram_vocab
    except:
        return []

def process_sentence(sentence):
    return '' + sentence + ''

def wrong_word(preword, word):
    for w in find_word_array_bigram(preword):
        if (w['w'] == word):
            return False
    return True

def find_pos_value_by_word(word, pos):
    for p in pos:
        if word == p['w']:
            return p['p']
    return 0

def fix_word(preword, word, afterword, list_fail, error = None, bigram = None):
    word_result = word
    pos_vocab = []
    if preword == 'preword' and bigram != None:
        bigram_pos = bigram
        error_pos = error
    else:
        error_pos, bigram_pos = find_pos(preword, word)

    for b in bigram_pos:
        if b['w'] not in list_fail:
            pos_vocab.append(b['w'])
    max = 0
    min_distance = 100

    for v in pos_vocab:
        if (len(bigram_pos)>0):
            ed_distance = edit_distance(v, word)
            if (min_distance>=ed_distance and ed_distance <= 2):
                if (min_distance == ed_distance):
                    tmp = find_pos_value_by_word(v, bigram_pos)
                    if (max < tmp):
                        max = tmp
                        word_result = v
                elif (min_distance > ed_distance):
                    max = 0
                    min_distance = ed_distance
                    word_result = v
    # tra ve ket qua
    if not wrong_word(word_result, afterword):
        return word_result
    if (word_result == word):
        try:
            return list_fail[0]
        except:
            return word
    if (afterword == 'afterword'):
        try:
            return word_result
        except:
            return word
    else:
        list_fail.append(word_result)
        return fix_word(preword, word, afterword, list_fail, error_pos, bigram_pos)

def check_spell_word(preword, word, afterword):
    if not wrong_word(word, afterword):
        return word
    if wrong_word(preword, word):
        return fix_word(preword, word, afterword, [])
    else:
        return word

# sentence = "những con người sống trên thanh pho"
# to_model_sentence = process_sentence(sentence)
# check_spell(sentence)
#
# sentence = "con người la giống loài ratt yeeu ớt"
# to_model_sentence = process_sentence(sentence)
# check_spell(sentence)
#
# sentence = "máy bay B52 không heer bẻ gãy ý chi của người lính coong sanr"
# to_model_sentence = process_sentence(sentence)
# check_spell(sentence)
#

def find_first_words(vocabs, words):
    rs = []
    for v in vocabs:
        dis = edit_distance(v, words)
        if  dis<=2 and dis != 0 :
            rs.append({
                'w': v,
                'p': dis
            })
    rs.sort(key=lambda x: x['p'])
    return rs
# rs = find_first_words(vocabs, 'thanh')

# sentence = 'thanh phố sox hữu rất nhiều'
# to_model_sentence = process_sentence(sentence)
# check_spell(sentence)

# sentence = "con người la giống loài ratt yeeu ớt"
# to_model_sentence = process_sentence(sentence)
# check_spell(sentence)
#
# sentence = "trắc trắn luôn"
# to_model_sentence = process_sentence(sentence)
# check_spell(sentence)

sentence = "sxung sướng"
to_model_sentence = process_sentence(sentence)
check_spell(sentence)