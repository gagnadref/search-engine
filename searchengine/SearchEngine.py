import Index
import nltk
import math
from collections import Counter

class SearchEngine:
	def __init__(self, index):
		self.index = index
		self.universe = range(0,len(self.index.index))

	def search(self, request):
		raise Exception("Abstract method search should have been implemented")

class BooleanSearchEngine(SearchEngine):
	# TODO: optimisation: traiter la requete par ordre de frequence croissante 
	# (memoriser la frequence dans le dictionnaire)
	def search(self, request):
		if request.value == "AND":
			return list(set(self.universe).intersection(*[set(self.search(r)) for r in request.children]))
		elif request.value == "OR":
			return list(set().union(*[set(self.search(r)) for r in request.children]))
		elif request.value == "NOT":
			return list(set(self.universe)-set(self.search(request.children[0])))
		else:
			return self.index.getIndexWithWord(request.value).keys()

class VectorSearchEngine(SearchEngine):
	def search(self, request):
		q = request.split()
		results = []
		for docid in self.universe:
			similarity = self.getSimilarity(docid, q)
			if similarity > 0.:
				results.append((docid,similarity))
		results.sort(key=lambda (doc, sim): sim, reverse=True)
		return [docid for (docid, sim) in results]

	def getSimilarity(self, docid, q):
		similarity = 0.
		for word in q:
			similarity+=self.index.getIndexWithDocidAndWord(docid,word)
		similarity/=math.sqrt(len(q))
		similarity/=self.index.getDocumentNorm(docid)
		return similarity

class ProbabilisticSearchEngine(VectorSearchEngine):
	def getSimilarity(self, docid, q):
		similarity = 0.
		for word in q:
			freq = self.index.getIndexWithDocidAndWord(docid,word)
			if freq > 0:
				idf = self.index.getIdf(docid, word)
				similarity += math.log(1+idf)*math.log(self.index.N/idf)
		return similarity

class DiceSearchEngine(VectorSearchEngine):
	def getSimilarity(self, docid, q):
		similarity = 0.
		for word in q:
			similarity+=self.index.getIndexWithDocidAndWord(docid,word)
		similarity*=2
		similarity/=self.index.getDocumentSize(docid)+len(q)
		return similarity

class JaccardSearchEngine(VectorSearchEngine):
	def getSimilarity(self, docid, q):
		similarity = 0.
		for word in q:
			similarity+=self.index.getIndexWithDocidAndWord(docid,word)
		similarity/=self.index.getDocumentSize(docid)+len(q)-similarity
		return similarity

class OverlapSearchEngine(VectorSearchEngine):
	def getSimilarity(self, docid, q):
		similarity = 0.
		for word in q:
			similarity+=self.index.getIndexWithDocidAndWord(docid,word)
		similarity/=min(self.index.getDocumentSize(docid),len(q))
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
		
