import os
from tqdm import tqdm

from config import *
from helper.functions import *
from Lexicon.lexicon import load_lexicon


def index():

	docIDs = generate_docIDs()

	lexicon = load_lexicon()

	try:
		with open(os.path.join(EXTRA_PATH, 'is_indexed.data'), "rb") as fp:
			is_indexed = pickle.load(fp)
	except FileNotFoundError:
		is_indexed = []


	tmpBarrels = [None] * NO_OF_BARRELS

	for file in tqdm(dataset_files()):
		
		doc_id = docIDs.get(file)

		print(str(doc_id) + "\n\n\n")
		if doc_id in is_indexed:
			continue
		
		words = parse_file(file)
				
		for position, word in enumerate(words):
			
			word_id = lexicon.get(word)
			barrel_num = int(word_id/BARREL_CAPACITY)

			if tmpBarrels[barrel_num] == None:
				tmpBarrels[barrel_num] = dict()
				
			
			print("wordid: {}  barrel number: {}".format(word_id, barrel_num))
			
			if doc_id not in tmpBarrels[barrel_num].keys():
				tmpBarrels[barrel_num][doc_id] = {}

			if word_id in tmpBarrels[barrel_num][doc_id]:
				tmpBarrels[barrel_num][doc_id][word_id].append(position)
			
			else:
				tmpBarrels[barrel_num][doc_id][word_id] = [position]

		
	fill_barrels(tmpBarrels)



		
