import os
from tqdm import tqdm
import time
from multiprocessing import Process

from config import *
from helper.functions import *
from Lexicon.lexicon import load_lexicon

from collections import defaultdict, OrderedDict  

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

	return inverted_barrel

def build_short_inverted_barrel(barrel_path):
	try:
		with open(barrel_path, 'r') as barrel_file:
			barrel = json.load(barrel_file)
			
	except Exception:
		print('Barrel: {} Failed'.format(barrel_path))
		
	
	# get file name for barrel
	barrel_name = barrel_path.split('/')[-1]

	inverted_barrel = invert_barrel(barrel)

	# Save Inverted Barrel
	with open(os.path.join(SHORT_INVERTED_BARRELS_PATH, barrel_name), 'w') as inverted_barrel_file:
			json.dump(inverted_barrel, inverted_barrel_file)

def build_inverted_barrel(barrel_path):
	try:
		with open(barrel_path, 'r') as barrel_file:
			barrel = json.load(barrel_file)
			
	except Exception:
		print('Barrel: {} Failed'.format(barrel_path))

	barrel_name = barrel_path.split('/')[-1]

	inverted_barrel = invert_barrel(barrel)

	with open(os.path.join(INVERTED_BARRELS_PATH, barrel_name), 'w') as inverted_barrel_file:
			json.dump(inverted_barrel, inverted_barrel_file)

def inverted_index():
	"""
	Takes barrels containing Forward Indices and produces barrels containing Inverted indices
	"""
	
	print("Building Inverted Index!")
	
	# For Short Barrels
	processes = []
	for barrel_path in tqdm(barrels(mode='forward', full=False)):
		
		processes.append(Process(target=build_short_inverted_barrel, args=(barrel_path,)))
		processes[-1].start()

	for p in processes:
		p.join()

	# For full barrels
	processes = []
	for barrel_path in tqdm(barrels(mode='forward', full=True)):

		processes.append(Process(target=build_inverted_barrel, args=(barrel_path,)))
		processes[-1].start()

	for p in processes:
		p.join()

	print("Inverted Index Complete!")
