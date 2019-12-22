import os
import json
from unidecode import unidecode
import string
import nltk
import pickle

from config import *

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag


def dataset_files():
	"""
		Generator to traverse through Dataset
		yeilds path of dataset files one by one
	"""

	for subdir, _, files in os.walk(DATA_PATH):
		
		subdir_path = os.path.abspath(subdir)

		#To specify range of files in each directory to index, add [:RANGE] after files
		for f in files[:100]:
			yield os.path.join(subdir_path, f)

def barrels(mode='forward', full=True):
	"""
		Generator to traverse through Barrels
		args:
			String mode: 'forward' or 'inverted'
			bool full: True for full barrels else short barrels
		
		yeilds path of files one by ones
	"""
	if full:
		if mode.lower() == 'forward':
			path = FORWARD_BARRELS_PATH
		elif mode.lower() == 'inverted':
			path = INVERTED_BARRELS_PATH
		else:
			return None
	else:
		if mode.lower() == 'forward':
			path = SHORT_FORWARD_BARRELS_PATH
		elif mode.lower() == 'inverted':
			path = SHORT_INVERTED_BARRELS_PATH
		else:
			return None
	

	for subdir, _, files in os.walk(path):
		
		subdir_path = os.path.abspath(subdir)

		for f in files:
			yield os.path.join(subdir_path, f)

def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

def parse_string(text):
	"""
	Function to clean string
	Tokenizes, stems and lematizes strings
	args:
		string text
	"""
	lemmatizer = WordNetLemmatizer()

	# Remove unicode characters
	text = unidecode(text)

	# Tokenize the sting to array of words while also removing any punctuation
	tokens = nltk.regexp_tokenize(text, r'\w+')
	
	final_tokens = []
	for token in tokens:
		if token.isdigit():
		# or token in stopwords.words('english'):
			continue

		# Lemmatize and Stem
		final_tokens.append(lemmatizer.lemmatize(token, pos=get_wordnet_pos(token)))
	
	return final_tokens

def parse_file(path, title=False):
	"""
	Function to parse files
	Opens files and clean the content
	args:
		path: path to the file
		title: part of file to parsed True for only title else text
	"""

	with open(path, 'r', encoding="utf8") as f:
		data = json.load(f)

	text = data['text'].lower()
	title_text = data['title'].lower()

	if title == True:
		return parse_string(title_text)

	return parse_string(text)

def get_docIDs():
	"""
		Indexes the files in the dataset folder
	"""

	try:
		with open(os.path.join(EXTRA_PATH, 'doc_ids.json'), "r") as fp:
			docIDs = json.load(fp)
	except FileNotFoundError:
		print("Could not find previous Doc IDs")
		print("Generating from scratch")
		docIDs = dict()

	# assign unique docids to new files
	current_max_id = len(docIDs.keys())
	for file in dataset_files():
		if docIDs.get(file) == None:
			docIDs[file] = current_max_id
			current_max_id += 1

	with open(os.path.join(EXTRA_PATH, 'doc_ids.json'), "w") as fp:
			json.dump(docIDs, fp)

	return docIDs

def fill_barrels(tempBarrels):
	"""
	Stores the Forward Indexed documents in their respective Barrels
	args:
		tempBarrels: dict with index of barrel as key and entries as values
	"""

	for index, barrel in tempBarrels.items():
		print("Adding: {} entries to barrel: {}".format(len(barrel), index))
		
		try:
			with open(os.path.join(FORWARD_BARRELS_PATH, "barrel_{}.json".format(index)), 'r') as barrel_file:
				barrel_content = json.load(barrel_file)
		except FileNotFoundError:
			barrel_content = {}

		print("Before appending: {} entries in barrel: {}".format(len(barrel_content), index))
		for key, value in barrel.items():
			barrel_content[key] = value
		
		print("After appending: {} entries in barrel: {}".format(len(barrel_content), index))
		with open(os.path.join(FORWARD_BARRELS_PATH, "barrel_{}.json".format(index)), 'w') as barrel_file:
				json.dump(barrel_content, barrel_file)

def fill_short_barrels(tempBarrels):	
	"""
	Stores the Forward Indexed titles in their respective Short Barrels
	args:
		tempBarrels: dict with index of barrel as key and entries as values
	"""
	for index, barrel in tempBarrels.items():
		print("Index: {}  short barrel length: {}".format(index, len(barrel)))
		
		try:
			with open(os.path.join(SHORT_FORWARD_BARRELS_PATH, "barrel_{}.json".format(index)), 'r') as barrel_file:
				barrel_content = json.load(barrel_file)
		except FileNotFoundError:
			barrel_content = {}

		for key, value in barrel.items():
			barrel_content[key] = value
		
		with open(os.path.join(SHORT_FORWARD_BARRELS_PATH, "barrel_{}.json".format(index)), 'w') as barrel_file:
				json.dump(barrel_content, barrel_file)

def load_barrel(barrel_id:int, mode='inverted', full=True):
	"""
		Function load load barrels in memory
		args:
			Integer barrel_id: barrel number to load
			String mode: 'forward' or 'inverted', Default 'inverted'
			bool full: True for full barrels else short barrels
		
	"""

	if full:
		if mode.lower() == 'forward':
			path = FORWARD_BARRELS_PATH
		elif mode.lower() == 'inverted':
			path = INVERTED_BARRELS_PATH
		else:
			return None
	else:
		if mode.lower() == 'forward':
			path = SHORT_FORWARD_BARRELS_PATH
		elif mode.lower() == 'inverted':
			path = SHORT_INVERTED_BARRELS_PATH
		else:
			return None
	
	barrel_path = os.path.join(path, "barrel_{}.json".format(barrel_id))

	try:
		with open(barrel_path, 'r') as barrel_file:
			return json.load(barrel_file)
	except FileNotFoundError:
		raise FileNotFoundError("Barrel \'{}\' does not exist at \'{}\'".format(barrel_id, barrel_path))
