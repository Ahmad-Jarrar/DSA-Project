import os
from tqdm import tqdm

from config import *
from helper.functions import *
from Lexicon.lexicon import load_lexicon

from collections import defaultdict, OrderedDict

# print(sorted(d.items(), key = lambda kv:(kv[1], kv[0])))  

def sorted_hitlist(hitlist):
	"""
	Orders docIDs according to No. of hits to speed up search and order according to importance
	args:
		hitlist: dict {docID:hits}
	returns: OrderedDict{docID:hits}
	"""
	order = sorted(hitlist, key = lambda key: len(hitlist[key]), reverse=True)
	return OrderedDict([(index, hitlist.get(index)) for index in order])


def invert_barrel(barrel):
	"""
	Takes barrel and inverts it to change mapping docID -> wordIDs -> hits
	to mapping wordID -> docIDs -> hits
	and then orders it
	args:
		barrel: dict {docID: wordIDs}
	returns: dict {wordID: docIDs}
	"""

	inverted_barrel = dict()

	for doc_id, hitlist in barrel.items():
		
		for word_id, hits in hitlist.items():
			
			if inverted_barrel.get(word_id) == None:
				inverted_barrel[word_id] = {}

			inverted_barrel[word_id][doc_id] = hits

	for word_id, hitlist in inverted_barrel.items():
		
		inverted_barrel[word_id] = sorted_hitlist(hitlist)

	return inverted_barrel

def inverted_index():
	"""
	Takes barrels containing Forward Indices and produces barrels containing Inverted indices
	"""
	
	print("Building Inverted Index!")

	for barrel_path in tqdm(barrels(mode='forward', full=False)):
		
		try:
			with open(barrel_path, 'r') as barrel_file:
				barrel = json.load(barrel_file)
				
		except Exception:
			print('Barrel: {} Failed'.format(barrel_path))
			continue

		barrel_name = barrel_path.split('/')[-1]

		inverted_barrel = invert_barrel(barrel)

		with open(os.path.join(SHORT_INVERTED_BARRELS_PATH, barrel_name), 'w') as inverted_barrel_file:
				json.dump(inverted_barrel, inverted_barrel_file)


	for barrel_path in tqdm(barrels(mode='forward', full=True)):
		
		try:
			with open(barrel_path, 'r') as barrel_file:
				barrel = json.load(barrel_file)
				
		except Exception:
			print('Barrel: {} Failed'.format(barrel_path))
			continue

		barrel_name = barrel_path.split('/')[-1]

		inverted_barrel = invert_barrel(barrel)

		with open(os.path.join(INVERTED_BARRELS_PATH, barrel_name), 'w') as inverted_barrel_file:
				json.dump(inverted_barrel, inverted_barrel_file)


	print("Inverted Index Complete!")
