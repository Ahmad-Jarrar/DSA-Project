import json
import os
from tqdm import tqdm
import time

# import multiprocessing
# from concurrent.futures import ThreadPoolExecutor

from helper.functions import *
from config import DATA_PATH, LEXICON_PATH, NO_OF_THREADS




def build_lexicon():

	try:
		with open(LEXICON_PATH, 'r', encoding='utf8') as lexicon_file:
			lexicon = json.load(lexicon_file)
			words = lexicon.keys()
	except FileNotFoundError:
		lexicon = dict()
		words = set()

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
		if file in is_included_in_lexicon:
			continue

		words = words.union(set(parse_file(file)))
		is_included_in_lexicon.append(file)

	# Change later
	for index, word in enumerate(words):
		lexicon[word] = index

	with open(LEXICON_PATH, 'w', encoding='utf8') as lexicon_file:
			json.dump(lexicon, lexicon_file)

	with open(os.path.join(EXTRA_PATH, 'added_to_lexicon.data'), "wb") as fp:   # Unpickling
			pickle.dump(is_included_in_lexicon,fp)

	return lexicon

def load_lexicon(update=False):
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