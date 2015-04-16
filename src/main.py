#! /usr/bin/python
# -*-coding:Utf-8 -*

import functions as F
import classes as C
import sys
import argparse

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
	answer = raw_input("Do you want to save the index on disk ? (y/n) ")
	if answer == "y":
		F.save(index, "./")
		print("Index saved.")
	else:
		print("Index not saved.")
        
        print("Entrez les requetes que vous voulez effectuer :")

        while True:
                requete = raw_input("\t>> ")
                searcher = C.Searcher()
                index = searcher.load("./")
                result = searcher.search(index, requete)
                print("Voici les résultats de la recherche : ")
              	if result is None:
              		print("\tAucun résultat ne correspond à la recherche.")
              	else:
                	for doc in result:
                		print("\t- " + doc)

main()
