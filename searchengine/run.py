import searchengine as SearchEngine
import index as Index

engineType = raw_input("Moteur de recherche?\n1: Booleen\n2: Vectoriel\n3: Probabiliste\n")
cacmFilename = raw_input("Chemin vers les documents bruts? (searchengine/resources/cacm.all)\n")
if cacmFilename == "":
	cacmFilename = "searchengine/resources/index.txt"
indexFilename = raw_input("Chemin vers l'index? (searchengine/resources/index.txt)\n")
if indexFilename == "":
	indexFilename = "searchengine/resources/index.txt"
commonWords = "searchengine/resources/common_words"
if engineType == "1":
	while True:
		request = raw_input("""Requete? (AND(department,OR(NOT(program),matrix)))\n""")
		if request == "":
			request = "AND(department,OR(NOT(program),matrix))"
		booleanRequest = SearchEngine.BooleanRequestParser().parse(request)
		index = Index.Index(cacmFilename,commonWords,indexFilename)
		searchEngine = SearchEngine.BooleanSearchEngine(index)
		result = searchEngine.search(booleanRequest)
		print(result[:10])
elif engineType == "2":
	indexType = raw_input("Ponderation?\n1: Frequence\n2: Frequence normalisee\n3: tf-idf\n")
	measureType = raw_input("Mesure de similarite?\n1: Cosinus\n2: Dice\n3: Jaccard\n4: Overlap\n")
	while True:
		request = raw_input("""Requete? (department matrix programming)\n""")
		if request == "":
			request = "department matrix programming"
		index = Index.Index()
		if indexType == "1":
			index = Index.Index(cacmFilename,commonWords,indexFilename)
		elif indexType == "2":
			index = Index.NormalizedIndex(cacmFilename,commonWords,indexFilename)
		elif indexType == "3":
			index = Index.TfIdfIndex(cacmFilename,commonWords,indexFilename)
		searchEngine = SearchEngine.VectorSearchEngine(index)
		if measureType == "2":
			searchEngine = SearchEngine.DiceSearchEngine(index)
		elif measureType == "3":
			searchEngine = SearchEngine.JaccardSearchEngine(index)
		elif measureType == "4":
			searchEngine = SearchEngine.OverlapSearchEngine(index)
		result = searchEngine.search(request)
		print(result[:10])
elif engineType == "3":
	while True:
		request = raw_input("""Requete? (department matrix programming)\n""")
		if request == "":
			request = "department matrix programming"
		index = Index.Index()
		index = Index.Index(cacmFilename,commonWords,indexFilename)
		searchEngine = SearchEngine.ProbabilisticSearchEngine(index)
		result = searchEngine.search(request)
		print(result[:10])