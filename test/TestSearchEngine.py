import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '../searchengine'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
import SearchEngine

class TestSearchEngine(unittest.TestCase):
	def test_BooleanRequestParser(self):
		request = "AND(department,OR(NOT(programming),matrix))"
		booleanRequest = SearchEngine.BooleanRequestParser().parse(request)
		expectedValue = SearchEngine.BooleanRequest("AND",[SearchEngine.BooleanRequest("department"),SearchEngine.BooleanRequest("OR",[SearchEngine.BooleanRequest("NOT",[SearchEngine.BooleanRequest("programming")]),SearchEngine.BooleanRequest("matrix")])])
		self.assertEqual(booleanRequest.getString(),expectedValue.getString())

	def test_BooleanSearchEngine(self):
		request = "AND(department,OR(NOT(program),matrix))"
		booleanRequest = SearchEngine.BooleanRequestParser().parse(request)
		searchEngine = SearchEngine.BooleanSearchEngine(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		result = searchEngine.search(booleanRequest)
		self.assertEqual(result,[1])

	def test_VectorSearchEngine(self):
		request = "department matrix programming"
		searchEngine = SearchEngine.VectorSearchEngine(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		result = searchEngine.search(request)
		self.assertEqual(result,[1,2])

if __name__ == "__main__":
	unittest.main()