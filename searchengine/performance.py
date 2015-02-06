import index as Index
import searchengine as SearchEngine
import time
import curve as Curve
import measure as Measure

class Performance:
	@classmethod
	def getSearchTime(cls, searchengine, testQueries):
		start = time.time()
		for testQuery in testQueries.testQueries:
			searchengine.search(testQuery.query)
		end = time.time()
		return round(end - start,2)

	@classmethod
	def compareSearchEngines(cls, listOfSearchEngines, testQueries, measure, filename):
		curves = []
		for searchEngine in listOfSearchEngines:
			curve = cls.testSearchEngine(searchEngine, testQueries, measure)
			curve.name = searchEngine.__class__.__name__ + "-" + searchEngine.index.__class__.__name__
			curves.append(curve)
		Curve.CSVFile.exportToCSV(curves, filename)

	@classmethod
	def compareMeasure(cls, searchEngine, testQueries, listOfMeasures, filename):
		curves = []
		for measure in listOfMeasures:
			curve = cls.testSearchEngine(searchEngine, testQueries, measure)
			curve.name = measure.__name__
			curves.append(curve)
		Curve.CSVFile.exportToCSV(curves, filename)

	@classmethod
	def testSearchEngine(cls, searchEngine, testQueries, measure):
		x = range(0,101)
		meanCurve = Curve.Curve(x, [0. for i in x])
		numberOfCurves = 0
		for testQuery in testQueries.testQueries:
			query = testQuery.query
			if len(testQuery.expectedResult) > 0:
				curve = cls.getCurve(searchEngine, testQuery, measure)
				if len(curve)>0:
					numberOfCurves += 1
					curve.removeWrongPoints()
					curve.extrapolate(x)
					meanCurve += curve
		meanCurve = (1./numberOfCurves) * meanCurve
		return meanCurve

	@classmethod
	def getCurve(cls, searchEngine, testQuery, measure):
		results = searchEngine.search(testQuery.query)
		relevant = len(testQuery.expectedResult)
		tp = [0 for i in range(0,len(results))]
		for j in range(0,len(results)):
			tp[j]=tp[max(0,j-1)]
			if results[j] in testQuery.expectedResult:
				tp[j]+=1
		curve = Curve.Curve([],[])
		for j in range(0,len(results)):
			if j==0 or tp[j]>tp[j-1]:
				fp = j+1-tp[j]
				fn = relevant-tp[j]
				curve.append(measure.getRecall(tp[j],fp,fn),measure.getMeasure(tp[j],fp,fn))
		return curve


class TestQueries:
	def __init__(self, queriesFilename, commonWords, expectedResultsFilename):
		queries = self._importQueries(queriesFilename, commonWords)
		expectedResults = self._importExpectedResults(expectedResultsFilename)
		self.testQueries = [TestQuery(queries[i],expectedResults.get(i+1,[])) for i in range(0,len(queries))]

	def _importQueries(self, filename, commonWords):
		queries = []
		with open(filename,"r") as cacmFile:
			listOfQueries = Index.Index.splitCACMFile(cacmFile)
		for query in listOfQueries:
			cacm = Index.CACMParser.parse(query)
			cacm.tokenize()
			cacm.removeCommonWords(commonWords)
			request = " ".join(cacm.tokens)
			queries.append(request)
		return queries

	def _importExpectedResults(self, filename):
		expectedResults = {}
		with open(filename, "r") as qrels:
			for line in qrels:
				query = int(line.split()[0])
				docid = int(line.split()[1])
				docids = expectedResults.get(query,[])
				docids.append(docid-1)
				expectedResults[query] = docids
		return expectedResults

	def __len__(self):
		return len(self.testQueries)


class TestQuery:
	def __init__(self, query, expectedResult):
		self.query = query
		self.expectedResult = expectedResult


if __name__ == "__main__":
	cacmFilename = "searchengine/resources/cacm.all"
	commonWords = "searchengine/resources/common_words"
	indexFilename = "searchengine/resources/index.txt"
	testQueries = TestQueries("searchengine/resources/query.text", commonWords, "searchengine/resources/qrels.text")
	
	index = Index.Index(cacmFilename, commonWords, indexFilename)
	normalizedIndex = Index.NormalizedIndex(cacmFilename, commonWords,indexFilename)
	tfidfIndex = Index.TfIdfIndex(cacmFilename, commonWords,indexFilename)

	vector_index = SearchEngine.VectorSearchEngine(index)
	dice_index = SearchEngine.DiceSearchEngine(index)
	jaccard_index = SearchEngine.JaccardSearchEngine(index)
	overlap_index = SearchEngine.OverlapSearchEngine(index)
	probabilistic_index = SearchEngine.ProbabilisticSearchEngine(index)

	vector_normalizedIndex = SearchEngine.VectorSearchEngine(normalizedIndex)
	vector_tfidfIndex = SearchEngine.VectorSearchEngine(tfidfIndex)

	searchTime = Performance.getSearchTime(probabilistic_index, testQueries)
	print("Temps d'execution des {0} requetes : {1}s".format(len(testQueries),searchTime))

	Performance.compareSearchEngines([vector_index, dice_index, jaccard_index, overlap_index, probabilistic_index], testQueries, Measure.Precision, "MesureSimilarite.csv")
	Performance.compareSearchEngines([vector_index, vector_normalizedIndex, vector_tfidfIndex], testQueries, Measure.Precision, "Ponderation.csv")
	Performance.compareMeasure(vector_index, testQueries, [Measure.Precision, Measure.FMeasure, Measure.EMeasure], "MesuresPerformance.csv")


