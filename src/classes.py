#! /usr/bin/python
# -*-coding:Utf-8 -*

import unicodedata
import re

class Document:
	def __init__(self, text, url):
		self.text = text
		self.url = url

	def show_text(self):
		print(self.text)

	def show_url(self):
		print(self.url)

class TokenizedDocument:
	def __init__(self, words, url):
		self.words = words
		self.url = url

	def show_words(self):
		i = 0
		result = ""
		for word in self.words:
			result += str(i) + ": " + word + "; "
			i += 1
		print(result)


"""types :
			- normalizer = 1
"""
class TextProcessor(object):
	def __init__(self, proc_type):
		self.proc_type = proc_type

	def get_type(self):
		if self.proc_type == 1:
			return "Normalizer"
		else:
			return ""

class Normalizer(TextProcessor):
	def __init__(self, proc_type):
		TextProcessor.__init__(self, proc_type)
		self.proc_type = proc_type

	def get_type(self):
		return TextProcessor.get_type(self)

	def process(self, word):
		result = ""
		temp = unicode(word, 'Utf-8')
		result = unicodedata.normalize('NFD', temp).encode('ascii', 'ignore')
		result = re.sub('[^a-zA-Z0-9]', '', result)
		return result.lower()

class GenderRemover(TextProcessor):
	def __init__(self, proc_type):
		TextProcessor.__init__(self, proc_type)
		self.proc_type = proc_type

	def process(self, word):
		result = ""
		if word == "la" or word == "les":
			result = "le"
		elif word == "ta" or word == "tes":
			result = "ton"
		return result

#on va dire que si le mot appartient à la liste de mots inutiles (dans config.py), on l'enlève
"""class UselessRemover(TextProcessor):
	def __init__(self, proc_type):
		TextProcessor.__init__(self, proc_type)
		self.proc_type = proc_type

	def process(self, words):
		result = []
		for word in words:
			if word 
		return result"""

#l'attribut wordToUrls sert à stocker, dans une map, des mots associés à des noms de fichiers
class Index:
	def __init__(self, wordToUrls):
		self.wordToUrls = wordToUrls


class Searcher:
        def __init__(self):

        def load(path):
                index = ""
                path = path + "index.pickle"
                with open(path, 'rb') as f:
                        index = pickle.load(f)
                return index

        def search(index, word):
                for li in index:
                        if li == word:
                                return li

        def serach(index, liste):
                result = []
                for word in liste:
                        for li in index:
                                if li == word:
                                        result.append(li)
                return result

