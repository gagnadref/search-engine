import SearchEngine
import Index

if __name__ == "__main__":
	searchType = raw_input("Type de recherche?\n1: Booleene\n2: Vectorielle\n")
	filename = raw_input("Chemin vers l'index ou les documents bruts? (searchengine/resources/index.txt)\n")
	if filename == "":
		filename = "searchengine/resources/index.txt"
	if searchType == "1":
		while True:
			request = raw_input("""Requete? (AND(department,OR(NOT(program),matrix)))\n""")
			if request == "":
				request = "AND(department,OR(NOT(program),matrix))"
			booleanRequest = SearchEngine.BooleanRequestParser().parse(request)
			searchEngine = SearchEngine.BooleanSearchEngine(filename,"searchengine/resources/common_words")
			result = searchEngine.search(booleanRequest)
			print(result)
	elif searchType == "2":
		while True:
			request = raw_input("""Requete? (department matrix programming)\n""")
			if request == "":
				request = "department matrix programming"
			searchEngine = SearchEngine.VectorSearchEngine(filename,"searchengine/resources/common_words")
			result = searchEngine.search(request)
			print(result)