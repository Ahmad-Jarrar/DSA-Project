import os
import json
from unidecode import unidecode
import string
import nltk
import pickle

from config import *

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer


def dataset_files():
	"""
		Generator to traverse through Dataset
	"""

	for subdir, _, files in os.walk(DATA_PATH):
		
		subdir_path = os.path.abspath(subdir)

		for f in files[:15000]:
			yield os.path.join(subdir_path, f)

def barrels(mode='forward', full=True):
	"""
		Generator to traverse through Dataset
		args:
			String mode: 'forward' or 'backward'
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
	

	for subdir, _, files in os.walk(path):
		
		subdir_path = os.path.abspath(subdir)

		for f in files:
			yield os.path.join(subdir_path, f)


def test_dataset_files():
	"""
		Testing function for generator function
		No more used
	"""
	file_names = []
	for file in dataset_files():
		print(file)
		file_names.append(file)

	print(len(file_names))

def parse_string(text):
	"""
	Function to clean string
	Tokenizes, stems and lematizes strings
	args:
		string text
	"""

	text = unidecode(text)
	tokens = nltk.regexp_tokenize(text, r'\w+')

	# Removed due to huge performance penalty
	# tokens = [token for token in tokens if not token in stopwords.words('english')]
	
	tokens = [token for token in tokens if not(token.isdigit())]
	
	stemmer = PorterStemmer()
	lemmatizer = WordNetLemmatizer()

	return [lemmatizer.lemmatize(stemmer.stem(token)) for token in tokens]

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

def generate_docIDs():
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