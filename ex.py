import csv
import json, pickle
import sys


def readData(fileName):
    data = []
    file = open(fileName, "r",encoding="utf8")

    for word in file.read().split():
        data.append(word)

    file.close()
    return data



def Bigramcreation(data):
	listOfBigrams = []
	bigramCounts = {}
	unigramCounts  = {}

	for  i  in  range ( len ( data )):
		if  i  <  len ( data ) -  1 :

			listOfBigrams.append((data[i], data[i + 1]))

			if (data[i], data[i+1]) in bigramCounts:
				bigramCounts[(data[i], data[i + 1])] += 1
			else:
				bigramCounts[(data[i], data[i + 1])] = 1

		if  data [ i ] in  unigramCounts :
			unigramCounts[data[i]] += 1
		else:
			unigramCounts[data[i]] = 1

	return listOfBigrams, unigramCounts, bigramCounts


# ------------------------------ Simple Bigram Model --------------------------------


def calcBigramProb(listOfBigrams, unigramCounts, bigramCounts):
    listOfProb = {}
    for bigram in listOfBigrams:
        word1 = bigram[0]
        word2 = bigram[1]

        listOfProb[bigram] = (bigramCounts.get(bigram)) / (unigramCounts.get(word1))



    return listOfProb


if __name__ == '__main__':


	data = readData('data.csv')
	listOfBigrams, unigramCounts, bigramCounts = Bigramcreation(data)
	bigramProb = calcBigramProb(listOfBigrams, unigramCounts, bigramCounts)

    print(bigramProb)