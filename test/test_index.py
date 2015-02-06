import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '../searchengine'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
import index as Index
import math

class TestIndex(unittest.TestCase):
	def setUp(self):
		self.test_document = """.I 1\n.T\nTechniques Department on Matrix Program Schemes\n.B\nCACM December, 1958\n.A\nFriedman, M. D.\n.N\nCA581201 JB March 22, 1978  8:30 PM\n.X\n1	5	1\n1	5	1\n1	5	1\n"""

	def test_splitCACMFile(self):
		index = Index.Index()
		listOfDocuments = []
		with open(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),"r") as cacmFile:
			listOfDocuments = index.splitCACMFile(cacmFile)
		self.assertEqual(listOfDocuments[0],self.test_document)

	def test_CACMParser(self):
		cacm = Index.CACMParser.parse(self.test_document)
		self.assertEqual(cacm.docid, 1)
		self.assertEqual(cacm.title, "Techniques Department on Matrix Program Schemes\n")
		self.assertEqual(cacm.publicationDate, "CACM December, 1958\n")
		self.assertEqual(cacm.authors, "Friedman, M. D.\n")
		self.assertEqual(cacm.insertionDate, "CA581201 JB March 22, 1978  8:30 PM\n")
		self.assertEqual(cacm.references, """1	5	1\n1	5	1\n1	5	1\n""")


	def test_createIndexFromCACMFile(self):
		index = Index.Index(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		self.assertEqual(index.getIndexWithDocid(0),{'depart': 1, 'program': 1, 'scheme': 1, 'matrix': 1, 'techniqu': 1})

	def test_reversedIndex(self):
		index = Index.Index(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		self.assertEqual(index.getIndexWithWord("depart"),{0:1})

	def test_persistIndex(self):
		index = Index.Index(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		index.persistIndex("test/resources/index.txt")
		json = ""
		with open("test/resources/index.txt","r") as persistedIndex:
			json = persistedIndex.read()
		self.assertEqual(json,"""[{"program": 1, "scheme": 1, "depart": 1, "techniqu": 1, "matrix": 1}, {"program": 1, "engin": 1, "glossari": 1, "of": 1, "comput": 2, "terminolog": 1}]""")

	def test_NormalizedIndex(self):
		normalizedIndex = Index.NormalizedIndex(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		self.assertEqual(normalizedIndex.index,[{'depart': 1., 'program': 1., 'scheme': 1., 'matrix': 1., 'techniqu': 1}, {'glossari': 0.5, 'of': 0.5, 'program': 0.5, 'engin': 0.5, 'comput': 1., 'terminolog': 0.5}])

	def test_getTfIdf(self):
		index = Index.Index(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		tfIdf = index.getTfIdf(1,"comput")
		self.assertEqual(tfIdf, math.log(3,10)*math.log(2,10))

	def test_getTfIdfIndex(self):
		tfIdfIndex = Index.TfIdfIndex(os.path.abspath(os.path.join(testdir, "resources/test_cacm.all")),os.path.abspath(os.path.join(testdir, "resources/common_words")))
		self.assertEqual(tfIdfIndex.index[1]["comput"],math.log(3,10)*math.log(2,10))

if __name__ == "__main__":
	unittest.main()