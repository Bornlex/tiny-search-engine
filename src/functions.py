#! /usr/bin/python
# -*-coding:Utf-8 -*

#les imports
import classes as C
import os
import pickle
import config as conf

#les variables globales
g_verbose = False

#on set les variables globales
def set_global(result):
	global g_verbose
	g_verbose = result.verbose

#on verifie s'il y a un / a la fin de l'argument
def remove_slash(arg):
	arg = arg.replace("/", "")
	return arg

#verification de l'extension
def check_extension(fichier):
	extensions_valides = ['txt', 'md'];
	tab = fichier.split(".");
	extension = tab[1];
	for ext in extensions_valides:
		if extension == ext or extension == ext.upper():
			return True
	return False

#on affiche simplement les chemins des documents de la liste
def print_url_documents(documents):
	for doc in documents:
		doc.show_url()

#on affiche le contenu des documents de la liste
def print_contenu_documents(documents):
	for doc in documents:
		doc.show_text()

#on affiche le contenu des documents tokenizés de la liste
def print_contenu_tokenized_documents(tokenized):
	for doc in tokenized:
		doc.show_words()

#la fonction qui renvoie la liste de ducuments lisibles
def fetch(path, recursive):
	global g_verbose
	recursive = True
	documents = []
	if os.path.exists(path) == False:
		return []
	fichiers = os.listdir(path)
	if g_verbose: print("Fetching from " + path + ":")
	for fichier in fichiers:
		if os.path.isdir(path + "/" + fichier):
			documents += fetch(path + "/" + fichier, True)
		elif check_extension(fichier) == True:
			if g_verbose: print("\t" + fichier)
			contenu = open(path + "/" + fichier, "r").read()
			doc = C.Document(contenu, path + "/" + fichier)
			documents.append(doc)	
	return documents 

#cree tous les processeurs et les met dans une liste
def create_processors():
	processors = []
	normalizer = C.Normalizer(1)
	processors.append(normalizer)
	return processors

#decoupe le texte du document en mots
def tokenize(document):
	tokens = document.text.split(" ")
	path = document.url
	return C.TokenizedDocument(tokens, path)

#transforme les documents en mots et effectue des traitements sur ces mots
def analyze(documents, processors):
	global g_verbose
	TokenizedDocs = []
	if g_verbose: print("\tTokenizing...")
	for doc in documents:
		tok_doc = tokenize(doc)
		TokenizedDocs.append(tok_doc)
	if g_verbose: print("\tTokenizing :                                        OK")
	if g_verbose: print("\tAnalyzing...")
	for doc in TokenizedDocs:
		temp = []
		for word in doc.words:
			for proc in processors:
				word = proc.process(word)
				temp.append(word)
				#ici, les token sont bien processés
		doc.words = temp
	if g_verbose: print("\tAnalyzing  :                                        OK")
	return TokenizedDocs

def build(TokenizedDocs):
	#creation du dictionnaire puis instanciation de l'index avec le dico comme attribut
	#tous les mots qui seront ignorés
	wordToUrls = {}
	for tok in TokenizedDocs:
		for word in tok.words:
			if word in wordToUrls:
				wordToUrls[word].append(tok.url)
			else:
				wordToUrls[word] = [tok.url]

	index = C.Index(wordToUrls)
	return index

#sauvegarde de l'index sur le disque
def save(index, path):
	path = "./"

	#sérialization
	with open('index.pickle', 'wb') as f:
		pickle.dump(index, f)
