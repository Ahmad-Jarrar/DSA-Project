import os
from tqdm import tqdm

from config import *
from helper.functions import *
from Lexicon.lexicon import load_lexicon


def insert_in_barrels(barrels, doc_id, words, lexicon):
	"""
	Generates hitlists and add entries of document in barrels according to words it contains
	args:
		barrels: dict of barrels {barrel_index : docIDs}
		doc_id: docID to add
		words: list of words the document contains
		lexicon: dict containing words and their word_id
	"""
	for position, word in enumerate(words):
		
		word_id = lexicon.get(word)
		if word_id == None:
			
			# Some very problematic words in titles
			# print(word)
			continue
		
		# calculate which barrel does the word belong
		barrel_num = int(word_id//BARREL_CAPACITY)

		# For first document in barrel create key for barrel number in dict
		if barrels.get(barrel_num) == None :
			barrels[barrel_num] = dict()
		
		# For first word in document in range of barrel create key for DocID in dict
		if barrels[barrel_num].get(doc_id) == None:
			barrels[barrel_num][doc_id] = {}

		# For first word occurence in document in range of barrel create hitlist in dict
		if barrels[barrel_num][doc_id].get(word_id) == None:
			barrels[barrel_num][doc_id][word_id] = [position]
		
		else:
		# Append position to hitlist
			barrels[barrel_num][doc_id][word_id].append(position)

	return barrels

def forward_index():
	"""
	Function to produce forward index of all documents in Dataset
	"""
	print("Building Forward Index!")

	# load dict containing {"file_name": DocID}
	docIDs = get_docIDs()

	# Load Lexicon
	lexicon = load_lexicon()

	# Load or make a new list of files already indexed
	try:
		with open(os.path.join(EXTRA_PATH, 'is_indexed.data'), "rb") as fp:
			is_indexed = pickle.load(fp)
	except FileNotFoundError:
		is_indexed = []

	# Create  temporary barrels to be merged in already stored barrels
	tmpBarrels = dict()
	tmpShortBarrels = dict()

	for file in tqdm(dataset_files()):
		
		doc_id = docIDs.get(file)

		# If file already indexed Skip it
		if doc_id in is_indexed:
			continue
		
		# get processed list of words in file
		words = parse_file(file)
		title_words = parse_file(file, title=True)
		
		# Insert file in temporary barrels
		tmpShortBarrels = insert_in_barrels(tmpShortBarrels, doc_id, title_words, lexicon)
		tmpBarrels = insert_in_barrels(tmpBarrels, doc_id, words, lexicon)
		
		# Mark as indexed
		is_indexed.append(doc_id)
	
	# Merge and store content of temporary barrels in orignal barrels
	fill_barrels(tmpBarrels)
	fill_short_barrels(tmpShortBarrels)

	with open(os.path.join(EXTRA_PATH, 'is_indexed.data'), "wb") as fp:
			pickle.dump(is_indexed, fp)

	print("Forward Indexing Complete!")
