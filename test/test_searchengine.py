import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '../searchengine'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
import searchengine as SearchEngine
import index as Index

class TestSearchEngine(unittest.TestCase):
	def test_BooleanRequestParser(self):
		request = "AND(department,OR(NOT(programming),matrix))"
		booleanRequest = SearchEngine.BooleanRequestParser().parse(request)
		expectedValue = SearchEngine.BooleanRequest("AND",[SearchEngine.BooleanRequest("depart"),SearchEngine.BooleanRequest("OR",[SearchEngine.BooleanRequest("NOT",[SearchEngine.BooleanRequest("program")]),SearchEngine.BooleanRequest("matrix")])])
		self.assertEqual(booleanRequest.getString(),expectedValue.getString())

	def test_BooleanSearchEngine(self):
		request = "AND(department,OR(NOT(program),matrix))"
		booleanRequest = SearchEngine.BooleanRequestParser().parse(request)
		index = Index.Index(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		searchEngine = SearchEngine.BooleanSearchEngine(index)
		result = searchEngine.search(booleanRequest)
		self.assertEqual(result,[0])

	def test_VectorSearchEngine(self):
		request = "department matrix programming"
		index = Index.Index(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		searchEngine = SearchEngine.VectorSearchEngine(index)
		result = searchEngine.search(request)
		self.assertEqual(result,[0])

	def test_searchWithTfIdf(self):
		request = "department matrix programming"
		index = Index.TfIdfIndex(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		searchEngine = SearchEngine.VectorSearchEngine(index)
		result = searchEngine.search(request)
		self.assertEqual(result,[0])

	def test_ProbabilsticSearchEngine(self):
		request = "department matrix programming"
		index = Index.Index(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		searchEngine = SearchEngine.ProbabilisticSearchEngine(index)
		result = searchEngine.search(request)
		self.assertEqual(result,[0])

	def test_DiceSearchEngine(self):
		request = "department matrix programming"
		index = Index.Index(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		searchEngine = SearchEngine.DiceSearchEngine(index)
		result = searchEngine.search(request)
		self.assertEqual(result,[0])

	def test_JaccardSearchEngine(self):
		request = "department matrix programming"
		index = Index.Index(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		searchEngine = SearchEngine.JaccardSearchEngine(index)
		result = searchEngine.search(request)
		self.assertEqual(result,[0])

	def test_OverlapSearchEngine(self):
		request = "department matrix programming"
		index = Index.Index(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		searchEngine = SearchEngine.OverlapSearchEngine(index)
		result = searchEngine.search(request)
		self.assertEqual(result,[0])

if __name__ == "__main__":
	unittest.main()