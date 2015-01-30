import os
import sys
import time
import Index
import SearchEngine

filename = "searchengine/resources/cacm.all"
t0 = time.time()
indexCacmAll = Index.Index(filename, "searchengine/resources/common_words")
t1 = time.time()
indexCacmAll.persistIndex("searchengine/resources/index.txt")
t2 = time.time()
indexFromFile = Index.Index("searchengine/resources/index.txt", "searchengine/resources/common_words")
t3 = time.time()
dt1 = round(t1 - t0,2)
dt2 = round(t3 - t2,2)
fileSize = round(float(os.path.getsize("searchengine/resources/index.txt"))/1000000,1)
indexSize = round(float(indexCacmAll.__sizeof__()/1000000),1)

print("Temps de calcul pour l'indexation : {0}s".format(dt1))
print("Temps de chargement de l'index depuis le disque : {0}s".format(dt2))
print("Taille de l'index sur le disque : {0}Mo".format(fileSize))
print("Taille de l'index en memoire : {0}Mo".format(indexSize))
