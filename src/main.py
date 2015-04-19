#! /usr/bin/python
# -*-coding:Utf-8 -*

import functions as F
import classes as C
import sys
import argparse
import operator
import os

g_verbose = False

def show_arg(result):
	show_url = ""
	show_text = ""
	verbose = ""
	if result.show_url:
		show_url = "True"
	else:
		show_url = "False"
	if result.show_text:
		show_text = "True"
	else:
		show_text = "False"
	if result.verbose:
		verbose = "True"
	else:
		verbose = "False"
	print "Arguments :"
	print "\t- Show_url : " + show_url
	print "\t- Show_text : " + show_text
	print "\t- Verbose : " + verbose
	print "\t- Path : " + result.path


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-path', action="store", dest="path", help="set the path", default=".")
	parser.add_argument('-show_url', action="store_true", dest="show_url", help="show path of fetched files", default=False)
	parser.add_argument('-show_text', action="store_true", dest="show_text", help="show content of fetched files", default=False)
	parser.add_argument('-Verbose', action="store_true", dest="verbose", help="show path of fetched files during fetching", default=False)
	parser.add_argument('-show_arg', action="store_true", dest="show_arg", help="show arguments", default=False)
	parser.add_argument('-version', action="version", version="%(prog)s 1.0")

	result = parser.parse_args()
	global g_verbose
	g_verbose = result.verbose
	if result.show_arg:
		show_arg(result)

	saved = 0
	print("Voulez-vous fabriquer un nouvel index (si aucun index existant ou nouvelle base de données) ? (y/n)")
	answ = raw_input(">> ")
	if answ == "y":
		old_path = result.path
		path = F.remove_slash(old_path)
		F.set_global(result)
		if g_verbose:
			print("--------------------------------------------------------------------------------")
			print("Fetching...")
		documents = F.fetch(path, True)
		if g_verbose:
			print("Fetching   :                                                OK")
			print("--------------------------------------------------------------------------------")
			print("--------------------------------------------------------------------------------")
			print("Processing...")
		processors = F.create_processors()
		tokenized = F.analyze(documents, processors)
		if g_verbose:
			print("Processing :                                                OK")
			print("--------------------------------------------------------------------------------")
		#F.print_contenu_tokenized_documents(tokenized)
		index = F.build(tokenized)
		answer = raw_input("Voulez-vous sauvegarder l'index sur le disque ? (y/n) ")
		if answer == "y":
			F.save(index, "./")
			print("Index sauvegardé.")
			saved = 1
		else:
			print("Index non sauvegardé.")
        
	searcher = C.Searcher()
	if saved == 0:
		print("Existe-t-il un index.pickle (src/index.pickle) ? (y/n)")
		ans = raw_input(">> ")
		if ans == "y":
			print("Chargement de l'index...")
			index = searcher.load("./")
		else:
			print("Il n'existe pas d'index et vous n'en avez pas chargez un, la recherche est impossible. Le programme va quitter.")
			return
	if saved == 1:
		print("Chargement de l'index...")
		index = searcher.load("./") #l'index soit se trouver dans le dossier src, se nommer index.pickle
	print("Entrez les requetes que vous voulez effectuer (les résultats sont triés par pertinence):")
	print("Indiquez 'stop!' pour arrêter la recherche")
	while True:
		requete = raw_input("\t>> ")
		requete_split = requete.split(' ', 1)
		if requete == "stop!":
			break
		results = searcher.search(index, requete_split)
		print("Voici les résultats de la recherche : ")
		if not results:
          		print("\tAucun résultat ne correspond à la recherche.")
          	else:
          		final = {}
          		for doc in results:
          			if doc in final:
          				final[doc] += 1
          			else:
          				final[doc] = 1
          		dico = sorted(final.items(), key=operator.itemgetter(1))
			for i in range(0, len(dico)):
				print("\t- " + dico[len(dico) - 1 - i][0] + " (" + str(dico[len(dico) - 1 - i][1]) + ")")

main()
