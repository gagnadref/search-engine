import Index
import nltk
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
		self.univers = range(1,len(self.index.index)+1)

	def search(self, request):
		q = request.split()
		similarities = []
		for docid in range(1,len(self.index.index)+1):
			similarities.append((docid,self.getSimilarity(docid, q)))
		similarities.sort(key=lambda (doc, sim): sim, reverse=True)
		return [docid for (docid, sim) in similarities]

	def getSimilarity(self, docid, q):
		similarity=0.
		for word in q:
			similarity+=self.index.getIndexWithDocidAndWord(docid,word)
		similarity/=len(q)
		similarity/=self.index.getDocumentSize(docid)
		return similarity


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
		
