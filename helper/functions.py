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
    for subdir, _, files in os.walk(DATA_PATH):
        
        subdir_path = os.path.abspath(subdir)

        for f in files[:500]:
            yield os.path.join(subdir_path, f)

def test_dataset_files():
    file_names = []
    for file in dataset_files():
        print(file)
        file_names.append(file)

    print(len(file_names))

def parse_file(path):

	with open(path, 'r', encoding="utf8") as f:
		data = json.load(f)

	text = data['text'].lower()

	text = unidecode(text)
	tokens = nltk.regexp_tokenize(text, r'\w+')

	# Removed due to huge performance penalty
	# tokens = [token for token in tokens if not token in stopwords.words('english')]
	
	tokens = [token for token in tokens if not(token.isdigit())]
	
	stemmer = PorterStemmer()
	lemmatizer = WordNetLemmatizer()

	tokens = [lemmatizer.lemmatize(stemmer.stem(token)) for token in tokens]

	return tokens


def generate_docIDs():
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
	for index, barrel in tempBarrels.items():
		print("Index: {}  barrel length: {}".format(index, len(barrel)))
		
		try:
			with open(os.path.join(BARRELS_PATH, "barrel_{}.json".format(index)), 'r') as barrel_file:
				barrel_content = json.load(barrel_file)
		except FileNotFoundError:
			barrel_content = {}

		for key, value in barrel.items():
			barrel_content[key] = value
		
		with open(os.path.join(BARRELS_PATH, "barrel_{}.json".format(index)), 'w') as barrel_file:
				json.dump(barrel_content, barrel_file)
