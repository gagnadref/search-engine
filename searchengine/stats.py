import os
import sys
import time
import index as Index
import searchengine as SearchEngine

class IndexStats:
	@staticmethod
	def getIndexationTime(index, filename, commonWords):
		start = time.time()
		indexCacmAll = index.__class__(filename, commonWords)
		end = time.time()
		return round(end - start,2)

	@staticmethod
	def getRecoveryTimeFromDisk(cacmFilename, commonWords, indexFilename):
		start = time.time()
		index = Index.Index(cacmFilename, commonWords, indexFilename)
		end = time.time()
		return round(end - start,2)

	@staticmethod
	def getIndexSizeOnDisk(indexFilename):
		return round(float(os.path.getsize(indexFilename))/1000000,1)

	@staticmethod
	def getIndexSizeInMemory(cacmFilename, commonWords, indexFilename):
		index = Index.Index(cacmFilename, commonWords, indexFilename)
		return round(float(index.__sizeof__()/1000000),1)

if __name__ == "__main__":
	cacmFilename = "searchengine/resources/cacm.all"
	commonWords = "searchengine/resources/common_words"
	indexFilename = "searchengine/resources/index.txt"

	indexationTime = IndexStats.getIndexationTime(Index.TfIdfIndex(), cacmFilename, commonWords)
	recoveryTimeFromDisk = IndexStats.getRecoveryTimeFromDisk(cacmFilename, commonWords, indexFilename)
	fileSize = IndexStats.getIndexSizeOnDisk(indexFilename)
	indexSize = IndexStats.getIndexSizeInMemory(cacmFilename, commonWords, indexFilename)

	print("Temps de calcul pour l'indexation : {0}s".format(indexationTime))
	print("Temps de chargement de l'index depuis le disque : {0}s".format(recoveryTimeFromDisk))
	print("Taille de l'index sur le disque : {0}Mo".format(fileSize))
	print("Taille de l'index en memoire : {0}Mo".format(indexSize))

