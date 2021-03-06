import sys
import nltk
import Stemmer
import math
from collections import Counter
import json

class Index:
	def __init__(self, cacmFilename="", commonWords="", indexFilename=""):
		if cacmFilename != "":
			self.commonWords = self.getCommonWords(commonWords)
			self.setListOfDocuments(cacmFilename)
			if  indexFilename=="":
				self.index = self.createIndexFromCACMFile()
			else:
				self.index = self.createIndexFromPersistedIndex(indexFilename)
			self.inversedIndex = self.inverseIndex()
			self.N = len(self.index)

	def __sizeof__(self):
		sizeof = sys.getsizeof(self.index)
		for doc in self.index:
			sizeof += sys.getsizeof(doc)
			for word, freq in doc.iteritems():
				sizeof += sys.getsizeof(word)
				sizeof += sys.getsizeof(freq)
		sizeof += sys.getsizeof(self.inversedIndex)
		for word, frequences in self.inversedIndex.iteritems():
			sizeof += sys.getsizeof(word)
			sizeof += sys.getsizeof(frequences)
			for docid, freq in frequences.iteritems():
				sizeof += sys.getsizeof(docid)
				sizeof += sys.getsizeof(freq)
		return sizeof


	def getCommonWords(self, filename): 
		commonWords = []
		with open(filename,"r") as commonWordsFile:
			for line in commonWordsFile:
				commonWords.append(line.rstrip())
		return commonWords

	def createIndexFromCACMFile(self):
		index = []
		for doc in self.listOfDocuments:
			cacm = CACMParser.parse(doc)
			cacm.tokenize()
			cacm.removeCommonWords(self.commonWords)
			cacm.stem()
			index.append(cacm.getFrequences())
		return index

	def createIndexFromPersistedIndex(self, indexFilename):
		index = []
		with open(indexFilename,"r") as persistedIndex:
			index = json.loads(persistedIndex.read())
		return index

	def persistIndex(self, filename):
		jsonIndex = json.dumps(self.index)
		with open(filename, "w") as persistedIndex:
			persistedIndex.write(jsonIndex)

	@classmethod
	def splitCACMFile(self, cacmFile):
		listOfDocuments = []
		currentDocument = ""
		for line in cacmFile:
			if line[:2]==".I":
				listOfDocuments.append(currentDocument)
				currentDocument = line
			else:
				currentDocument += line
		listOfDocuments.append(currentDocument)
		return listOfDocuments[1:]

	def inverseIndex(self):
		inversedIndex = {}
		for docid, frequences in enumerate(self.index):
			for word, freq in frequences.iteritems():
				inversedIndex[word] = inversedIndex.get(word, {})
				inversedIndex[word][docid] = freq
		return inversedIndex

	def getIndexWithDocid(self, docid):
		return self.index[docid]

	def getIndexWithWord(self, word):
		return self.inversedIndex.get(word,{})

	def getIndexWithDocidAndWord(self, docid, word):
		return self.index[docid].get(word,0)

	def getDocumentNorm(self, docid):
		norm = 0
		for word, freq in self.getIndexWithDocid(docid).iteritems():
			norm+=freq*freq
		return math.sqrt(norm)

	def getTf(self, docid, word):
		return self.getIndexWithDocidAndWord(docid,word)

	def getIdf(self, docid, word):
		return len(self.getIndexWithWord(word))

	def getTfIdf(self, docid, word):
		tf = self.getTf(docid, word)
		idf = self.getIdf(docid, word)
		tfidf=0.
		if tf>0:
			tfidf=math.log(1+tf,10)*math.log(self.N/idf,10)
		return tfidf

	def getDocumentSize(self, docid):
		size = 0
		for word, freq in self.getIndexWithDocid(docid).iteritems():
			size+=freq
		return size

	def setListOfDocuments(self, cacmFilename):
		with open(cacmFilename,"r") as cacmFile:
			self.listOfDocuments = self.splitCACMFile(cacmFile)

	def getDocument(self, docid):
		return self.listOfDocuments[docid]


class NormalizedIndex(Index):
	def __init__(self, cacmFilename="", commonWords="", indexFilename=""):
		Index.__init__(self, cacmFilename, commonWords, indexFilename)
		if cacmFilename != "":
			self.index = self.getNormalizedIndex()
			self.inversedIndex = self.inverseIndex()

	def getNormalizedIndex(self):
		normalizedFrequenceIndex = range(0,self.N)
		for docid, frequences in enumerate(self.index):
			maxFreq = 0
			for word, freq in frequences.iteritems():
				if freq > maxFreq:
					maxFreq = freq
			doc = {}
			for word, freq in frequences.iteritems():
				doc[word] = freq/float(maxFreq)
			normalizedFrequenceIndex[docid] = doc
		return normalizedFrequenceIndex


class TfIdfIndex(Index):
	def __init__(self, cacmFilename="", commonWords="", indexFilename=""):
		Index.__init__(self, cacmFilename, commonWords, indexFilename)
		if cacmFilename != "":
			self.index = self.getTfIdfIndex()
			self.inversedIndex = self.inverseIndex()

	def getTfIdfIndex(self):
		tfIdfIndex = range(0,self.N)
		for docid, frequences in enumerate(self.index):
			doc = {}
			for word in frequences:
				doc[word] = self.getTfIdf(docid, word)
			tfIdfIndex[docid] = doc
		return tfIdfIndex


			
class CACM:
	def __init__(self, docid=0, title="", summary="", publicationDate="", authors="", insertionDate="", references="", keyWords="", tokens=[]):
		self.docid = docid
		self.title = title
		self.summary = summary
		self.publicationDate = publicationDate
		self.authors = authors
		self.insertionDate = insertionDate
		self.references = references
		self.keyWords = keyWords
		self.tokens = tokens

	def tokenize(self):
		self.tokens = []
		tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')
		self.tokens += tokenizer.tokenize(self.title.lower())
		self.tokens += tokenizer.tokenize(self.summary.lower())
		self.tokens += tokenizer.tokenize(self.keyWords.lower())

	def stem(self):
		stemmer = Stemmer.Stemmer('english') 
		self.tokens = map(stemmer.stemWord, self.tokens)

	def removeCommonWords(self, commonWords) :
		self.tokens = [word for word in self.tokens if word not in commonWords]

	def getFrequences(self):
		return dict(Counter(self.tokens))

class CACMParser:
	@classmethod
	def parse(cls, doc):
		docid = 0
		title = ""
		summary = ""
		publicationDate = ""
		authors = ""
		insertionDate = ""
		references = ""
		keyWords = ""
		currentPattern = ""
		currentProperty = ""

		for line in doc.splitlines():
			line += "\n"
			if line[:2]==".I":
				docid = line[3:]
				currentPattern = ""
				currentProperty = ""
			elif line[:2] in [".T",".W",".B",".A",".N",".X",".K"]:
				if currentProperty != "":
					if currentPattern==".T":
						title = currentProperty
					elif currentPattern==".W":
						summary = currentProperty
					elif currentPattern==".B":
						publicationDate = currentProperty
					elif currentPattern==".A":
						authors = currentProperty
					elif currentPattern==".N":
						insertionDate = currentProperty
					elif currentPattern==".X":
						references = currentProperty
					elif currentPattern==".K":
						keyWords = currentProperty
				currentPattern = line[:2]
				currentProperty = ""
			else:
				currentProperty += line
		if currentProperty != "":
			if currentPattern==".T":
				title = currentProperty
			elif currentPattern==".W":
				summary = currentProperty
			elif currentPattern==".B":
				publicationDate = currentProperty
			elif currentPattern==".A":
				authors = currentProperty
			elif currentPattern==".N":
				insertionDate = currentProperty
			elif currentPattern==".X":
				references = currentProperty
			elif currentPattern==".K":
				keyWords = currentProperty

		return CACM(int(docid), title, summary, publicationDate, authors, insertionDate, references, keyWords)

