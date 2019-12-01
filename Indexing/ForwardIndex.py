import os
from tqdm import tqdm

from config import *
from helper.functions import *
from Lexicon.lexicon import load_lexicon


def insert_in_barrels(barrels, doc_id, words, lexicon):

	for position, word in enumerate(words):
		
		word_id = lexicon.get(word)
		if word_id == None:
			
			# Some very problematic words in titles
			# print(word)
			continue

		barrel_num = int(word_id//BARREL_CAPACITY)

		if barrels.get(barrel_num) == None :
			barrels[barrel_num] = dict()
		
		if barrels[barrel_num].get(doc_id) == None:
			barrels[barrel_num][doc_id] = {}

		if barrels[barrel_num][doc_id].get(word_id) == None:
			barrels[barrel_num][doc_id][word_id] = [position]
		
		else:
			barrels[barrel_num][doc_id][word_id].append(position)

	return barrels

def forward_index():
	print("Building Forward Index!")

	docIDs = generate_docIDs()

	lexicon = load_lexicon()

	try:
		with open(os.path.join(EXTRA_PATH, 'is_indexed.data'), "rb") as fp:
			is_indexed = pickle.load(fp)
	except FileNotFoundError:
		is_indexed = []


	tmpBarrels = dict()
	tmpShortBarrels = dict()

	for file in tqdm(dataset_files()):
		
		doc_id = docIDs.get(file)

		if doc_id in is_indexed:
			continue
		
		words = parse_file(file)
		title_words = parse_file(file, title=True)
		
		tmpShortBarrels = insert_in_barrels(tmpShortBarrels, doc_id, title_words, lexicon)
		tmpBarrels = insert_in_barrels(tmpBarrels, doc_id, words, lexicon)
		
		is_indexed.append(doc_id)
		
	fill_barrels(tmpBarrels)
	fill_short_barrels(tmpShortBarrels)

	with open(os.path.join(EXTRA_PATH, 'is_indexed.data'), "wb") as fp:
			pickle.dump(is_indexed, fp)

	print("Forward Indexing Complete!")
