import nltk
from collections import Counter

class Index:
	def __init__(self, documents="", commonWords=""):
		if documents != "":
			self.commonWords = self.getCommonWords(commonWords)
			self.index = self.createIndexFromCACMFile(documents)
			self.inversedIndex = self.inverseIndex()
			self.documentSizes = {}

	def getCommonWords(self, filename): 
		commonWords = []
		with open(filename,"r") as commonWordsFile:
			for line in commonWordsFile:
				commonWords.append(line.rstrip())
		return commonWords

	def createIndexFromCACMFile(self,filename):
		index = []
		with open(filename,"r") as cacmFile:
			listOfDocuments = self.splitCACMFile(cacmFile)
		for doc in listOfDocuments:
			cacm = CACMParser.parse(doc)
			cacm.tokenize()
			cacm.removeCommonWords(self.commonWords)
			index.append(cacm.getFrequences())
		return index

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
				inversedIndex[word][docid+1] = freq
		return inversedIndex

	def getIndexWithDocid(self, docid):
		return self.index[docid-1]

	def getIndexWithWord(self, word):
		return self.inversedIndex.get(word,0)
		# return self.inversedIndex[word]

	def getIndexWithDocidAndWord(self, docid, word):
		return self.index[docid-1].get(word,0)
		# return self.index[docid-1][word]

	def getDocumentSize(self, docid):
		if docid not in self.documentSizes:
			self.documentSizes[docid] = 0
			for word, freq in self.getIndexWithDocid(docid).iteritems():
				self.documentSizes[docid]+=freq
		return self.documentSizes[docid]

# class IndexBuilder:
# 	def createIndex(self, path):
# 		raise Exception("Abstract method createIndex should have been implemented")

# class CACMIndexBuilder(IndexBuilder):
# 	def createIndex(self, path):
# 		index = Index()
# 		index.index = self.createIndexFromCACMFile(path)

# 	def createIndexFromCACMFile(self,filename):
# 		index = []
# 		with open(filename,"r") as cacmFile:
# 			listOfDocuments = self.splitCACMFile(cacmFile)
# 		for doc in listOfDocuments:
# 			cacm = CACMParser.parse(doc)
# 			cacm.tokenize()
# 			cacm.removeCommonWords(self.commonWords)
# 			index.append(cacm.getFrequences())
# 		return index

			
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
		self.tokens += nltk.word_tokenize(self.title.lower())
		self.tokens += nltk.word_tokenize(self.summary.lower())
		self.tokens += nltk.word_tokenize(self.keyWords.lower())

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

