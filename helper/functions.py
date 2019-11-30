import os
import json
from unidecode import unidecode
import string
import nltk

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