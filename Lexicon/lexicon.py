import json
import os
import string
from tqdm import tqdm
import time

from functools import partial
import multiprocessing
import concurrent.futures

#from helper import generators
#from config import DATA_PATH, LEXICON_PATH, NO_OF_THREADS

DATA_PATH = '/home/ahmad/Desktop/DSA/DSA-Project/Data'
LEXICON_PATH = '/home/ahmad/Desktop/DSA/DSA-Project/Lexicon/lexicon.json'

def files():
    for subdir, _, files in os.walk(DATA_PATH):
        
        subdir_path = os.path.abspath(subdir)

        for f in files[:10000]:
            yield os.path.join(subdir_path, f)

def parse_file(path):

	# Get lock to synchronize threads
	try:
		with open(path, 'r', encoding="utf8") as f:
			data = json.load(f)

		text = data['text']

		translator = str.maketrans('', '', string.punctuation)
		text = text.lower().replace("-", " ").replace('\u201c', "").replace('\u201d', "").translate(translator)
		tokens = text.replace('\u2018', "").replace('\u2019', "").split()
		
		return set([token.lower() for token in tokens if token.isalpha()])

	except Exception:
		print("Failed: " + path)


def build_lexicon():
	words = set()
	lexicon = {}

	#MultiProcessing 134s 10000 files
	# with multiprocessing.Pool(8) as pool:
	# 	results = pool.map(parse_file, [file for file in files()])

	# for result in results:
	# 	words = words.union(result)
 
	#Single Threaded 115s 10000 files
	# for file in files():
	# 	words = words.union(parse_file(file))

	#MultiThreaded
	


	for index, word in enumerate(words):
		lexicon[word] = index

	with open(LEXICON_PATH, 'w', encoding='utf8') as lexicon_file:
		json.dump(lexicon, lexicon_file)

if __name__ == "__main__":
	
	start = time.time()
	build_lexicon()
	end = time.time()
	print("Time taken {}".format(end - start))