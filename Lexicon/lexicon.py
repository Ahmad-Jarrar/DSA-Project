import json
import os
from tqdm import tqdm
import time

# import multiprocessing
# from concurrent.futures import ThreadPoolExecutor

from helper.functions import *
from config import DATA_PATH, LEXICON_PATH, NO_OF_THREADS

def build_lexicon():
	"""
	Produces a lexicon containing all the words contained in text of documents in Dataset

	returns: dict {word: word_id}
	"""
	print("Building Lexicon!")

	# If some lexicon already exist load it
	try:
		with open(LEXICON_PATH, 'r', encoding='utf8') as lexicon_file:
			lexicon = json.load(lexicon_file)
			words_in_lexicon = set(lexicon.keys())
	except FileNotFoundError:
		lexicon = dict()
		words_in_lexicon = set()
	
	
	words = set()

	# To keep track of files already looked into to build lexicon, useful to update lexicon
	try:
		with open(os.path.join(EXTRA_PATH, 'added_to_lexicon.data'), "rb") as fp:   # Unpickling
			is_included_in_lexicon = pickle.load(fp)
	except FileNotFoundError:
		is_included_in_lexicon = []

	#MultiProcessing 134s 10000 files
	# with multiprocessing.Pool(8) as pool:
	# 	results = pool.map(parse_file, [file for file in files()])

	# for result in results:
	# 	words = words.union(result)

	#MultiThreaded 140s 10000 files
	# with ThreadPoolExecutor(4) as executor:
	# 	results = executor.map(parse_file, [file for file in files()])

	# for result in results:
	# 	words = words.union(result)
 
	#Single Threaded 115s 10000 files
	for file in tqdm(dataset_files()):
		# Skip if already looked into
		if file in is_included_in_lexicon:
			continue
		
		# Make create a set of all the words obtained, to remove duplicate
		words = words.union(set(parse_file(file)))
		is_included_in_lexicon.append(file)

	bias = len(words_in_lexicon)
	words = [word for word in words if lexicon.get(word) == None]
	for index, word in enumerate(words):
		lexicon[word] = index + bias

	with open(LEXICON_PATH, 'w', encoding='utf8') as lexicon_file:
			json.dump(lexicon, lexicon_file)

	with open(os.path.join(EXTRA_PATH, 'added_to_lexicon.data'), "wb") as fp:   # Unpickling
			pickle.dump(is_included_in_lexicon,fp)

	print("Lexicon Complete!")
	print("Lexicon Length: " + str(len(lexicon)))
	return lexicon

def load_lexicon(update=False):
	"""
	Load lexicon into memory
	args:
		bool update: if True, looks into dataset to look if new documents added which might have new words
	returns: dict {word : word_id}
	"""
	if update == True:
		return build_lexicon()
		
	try:
		with open(LEXICON_PATH, 'r', encoding='utf8') as lexicon_file:
			return json.load(lexicon_file)
	except Exception:
		print("Lexicon not found!")
		print("Building Lexicon from data in config path")

		return build_lexicon()


if __name__ == "__main__":
	
	start = time.time()
	build_lexicon()
	end = time.time()
	print("Time taken {}".format(end - start))