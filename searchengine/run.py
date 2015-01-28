import SearchEngine
import Index

if __name__ == "__main__":
	engineType = raw_input("Moteur de recherche?\n1: Booleen\n2: Vectoriel\n")
	filename = raw_input("Chemin vers l'index ou les documents bruts? (searchengine/resources/index.txt)\n")
	if filename == "":
		filename = "searchengine/resources/index.txt"
	if engineType == "1":
		while True:
			request = raw_input("""Requete? (AND(department,OR(NOT(program),matrix)))\n""")
			if request == "":
				request = "AND(department,OR(NOT(program),matrix))"
			booleanRequest = SearchEngine.BooleanRequestParser().parse(request)
			searchEngine = SearchEngine.BooleanSearchEngine(filename,"searchengine/resources/common_words")
			result = searchEngine.search(booleanRequest)
			print(result)()
	elif engineType == "2":
		indexType = raw_input("Ponderation?\n1: Frequence\n2: Frequence normalisee\n3: tf-idf\n")
		while True:
			request = raw_input("""Requete? (department matrix programming)\n""")
			if request == "":
				request = "department matrix programming"
			index = Index.Index()
			if indexType == "1":
				index = Index.Index(filename,"searchengine/resources/common_words")
			elif indexType == "2":
				index = Index.NormalizedIndex(filename,"searchengine/resources/common_words")
			elif indexType == "3":
				index = Index.TfIdfIndex(filename,"searchengine/resources/common_words")
			searchEngine = SearchEngine.VectorSearchEngine(index)
			result = searchEngine.search(request)
			print(result)