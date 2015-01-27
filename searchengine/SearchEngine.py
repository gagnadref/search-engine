import Index
import nltk
import math
from collections import Counter

class SearchEngine:
	def search(self, request):
		raise Exception("Abstract method search should have been implemented")

class BooleanSearchEngine(SearchEngine):
	def __init__(self, documents, commonWords):
		self.index = Index.Index(documents, commonWords)
		self.univers = range(1,len(self.index.index)+1)
	
	# TODO: optimisation: traiter la requete par ordre de frequence croissante 
	# (memoriser la frequence dans le dictionnaire)
	def search(self, request):
		if request.value == "AND":
			return list(set(self.univers).intersection(*[set(self.search(r)) for r in request.children]))
		elif request.value == "OR":
			return list(set().union(*[set(self.search(r)) for r in request.children]))
		elif request.value == "NOT":
			return list(set(self.univers)-set(self.search(request.children[0])))
		else:
			return self.index.getIndexWithWord(request.value).keys()

class VectorSearchEngine(SearchEngine):
	def __init__(self, documents, commonWords):
		self.index = Index.Index(documents, commonWords)
		self.univers = range(1,self.index.N)

	def search(self, request):
		similarities = []
		for docid in range(1,len(self.index.index)+1):
			similarities.append((docid,self.getSimilarity(docid, request)))
		similarities.sort(key=lambda (doc, sim): sim, reverse=True)
		return [docid for (docid, sim) in similarities]

	def searchWithTfIdf(self, request):
		similarities = []
		for docid in range(1,len(self.index.index)+1):
			similarities.append((docid,self.getTfIdfSimilarity(docid, request)))
		similarities.sort(key=lambda (doc, sim): sim, reverse=True)
		print(similarities)
		return [docid for (docid, sim) in similarities]

	def getSimilarity(self, docid, request):
		similarity=0.
		for word in request.tf:
			similarity+=request.tf[word]*self.index.getIndexWithDocidAndWord(docid,word)
		similarity/=request.norm
		similarity/=self.index.getDocumentNorm(docid)
		return similarity

	def getTfIdfSimilarity(self, docid, request):
		similarity=0.
		for word in request.tf:
			similarity+=self.index.getTfIdf(docid,word)
		similarity/=request.norm
		similarity/=self.index.getTfIdfNorm(docid)
		return similarity

class Request:
	def __init__(self, request):
		self.request = request
		self.tokens = nltk.word_tokenize(request.lower())
		self.tf = dict(Counter(self.tokens))
		self.norm = 0.


class BooleanRequest:
	def __init__(self, value, children = []):
		self.value = value
		self.children = children

	def getString(self):
		s = self.value
		if self.children:
			s += "("
			s += ",".join(map(BooleanRequest.getString,self.children))
			s += ")"
		return s

class BooleanRequestParser:
	def parse(self, request):
		if request[:4]=="AND(":
			return BooleanRequest("AND",map(self.parse, self.split(request[4:-1])))
		elif request[:3]=="OR(":
			return BooleanRequest("OR",map(self.parse, self.split(request[3:-1])))
		elif request[:4]=="NOT(":
			return BooleanRequest("NOT",[self.parse(request[4:-1])])
		else:
			return BooleanRequest(request)

	def split(self,s):
		acc=[]
		lastComma=0
		count = 0
		for i, c in enumerate(s):
			if c=="," and count==0:
				acc.append(s[lastComma:i])
				lastComma = i+1
			elif c=="(":
				count+=1
			elif c==")":
				count-=1
		acc.append(s[lastComma:])
		return acc
		
if __name__ == "__main__":
	searchType = raw_input("Type de recherche?\n1: Booleene\n2: Vectorielle\n")
	filename = raw_input("Chemin vers l'index ou les documents bruts? (searchengine/resources/cacm.all)\n")
	if filename == "":
		filename = "searchengine/resources/cacm.all"
	if searchType == "1":
		request = raw_input("""Requete? (AND(department,OR(NOT(program),matrix)))\n""")
		if request == "":
			request = "AND(department,OR(NOT(program),matrix))"
		booleanRequest = BooleanRequestParser().parse(request)
		searchEngine = BooleanSearchEngine(filename,"searchengine/resources/common_words")
		result = searchEngine.search(booleanRequest)
		searchEngine.index.persistIndex("searchengine/resources/index.txt")
		print(result)
	elif searchType == "2":
		request = raw_input("""Requete? (department matrix programming)\n""")
		if request == "":
			request = "department matrix programming"
		searchEngine = VectorSearchEngine(filename,"searchengine/resources/common_words")
		result = searchEngine.search(request)
		print(result)

