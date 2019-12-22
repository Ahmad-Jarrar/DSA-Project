from bidict import bidict

from config import *
from helper.functions import *
from Lexicon.lexicon import load_lexicon

class Searcher():

	def __init__(self):
		# Todo make bidict
		docIDs = get_docIDs()

		self.doc_ids = bidict(docIDs)
		
		self.lexicon = load_lexicon()

		self.loaded_barrels = {}
		self.loaded_short_barrels = {}

	# Done
	def single_word_query(self, word, raw=False):
		"""
			Takes one word and returns a dict of DocIDs and the respective Hitlists or ranks
			Args:
				String word: Word to be searched
				Bool raw: If True returns the raw results else ranks them first
			Returns:
				if raw=True: DocIDs and the respective Hitlists
				else DocIDs and ranks
		"""
		word_id = self.lexicon.get(word)
		
		if word == None:
			raise Exception("Word \'{}\' not found in lexicon".format(word))

		# calculate which barrel does the word belong
		barrel_num = int(word_id//BARREL_CAPACITY)
		
		if self.loaded_barrels.get(barrel_num) == None:
			
			try:
				self.loaded_barrels[barrel_num] = load_barrel(barrel_num)
			except Exception as e:
				print(e.with_traceback())

		if self.loaded_short_barrels.get(barrel_num) == None:
			
			try:
				self.loaded_short_barrels[barrel_num] = load_barrel(barrel_num, full=False)
			except Exception as e:
				print(e.with_traceback())

		title_hits = self.loaded_short_barrels.get(barrel_num).get(word_id)
		hits = self.loaded_barrels.get(barrel_num).get(word_id)
		
		total_hits = {'title_hits':title_hits, 'hits':hits}
		if raw:
			return total_hits

		return self.single_word_rank(total_hits)

	# Done	
	def multi_word_query(self, words):
		"""
			Takes list of words and returns a dict of DocIDs and ranks
			Args:
				String word: Word to be searched
		"""
		hits = []
		for word in words:
			hits.append(self.single_word_query(word))

		return self.multi_word_rank(hits)

	# Done
	def single_word_rank(self, hits:dict, alpha=1., beta=0.3):
		"""
		Take a dict  as {'title_hits':title_hits, 'hits':hits}
		and Ranks documnent according to the hits
		Different kinds of hits are weighted differently
		Args:
			dict hits: dict containing title_hits and hits
			float alpha: weight of title hit range(0, 1), Default=1.
			float beta: weight of normal hit range(0, 1), Default=0.1
		Returns:
			dict ranks: {docID: rank}
		Basic functionality, can be upgraded later
		"""
		ranks = {}

		for docID, hitlist in hits.get("title_hits").items():
			
			if ranks.get(docID) == None:
				ranks[docID] = 0

			ranks[docID] += len(hitlist) * alpha

		for docID, hitlist in hits.get("hits").items():
			
			if ranks.get(docID) == None:
				ranks[docID] = 0

			ranks[docID] += len(hitlist) * beta

		return ranks

	# Done
	def multi_word_rank(self, rankings, alpha=0.8):
		"""
		Take a list of dicts as [{docIDs: ranks},]
		coresponding to single word ranks for each word in query
		and Ranks documnent according to the hits
		Different kinds of hits are weighted differently
		Args:
			list rankings: list containing ranks for each word
			float alpha: weight docID containing multiple words range(0, 1), Default=0.8
		Returns:
			dict ranks: {docID: rank}
		Basic functionality, can be upgraded later
		"""
		ranks = {}

		for ranks_for_word in rankings:
			
			for docID, rank in ranks_for_word.items():
				
				if ranks.get(docID) == None:
					ranks[docID] = 0
				
				ranks[docID] += rank * alpha

		return ranks
		
	# Done
	def get_docs(self, docIDs, load=True, limit=20):
		"""
			Function to return the names of documents in search results from their docID
			Args:
				list docIDs: list of document ids
				bool load: if True load the content of files in memory to display
				int limit: limit the number of documents returned
			Returns:
				List: if load=True: content(in dict) else path of the files
		"""
		documents = []

		for doc_id in docIDs:
			file_path = self.doc_ids.inverse(doc_id)

			if load:
				try:
					with open(file_path, "r") as fp:
						documents.append(json.load(fp))
				except FileNotFoundError:
					pass
			else:
				documents.append(file_path)

			if len(documents) == limit:
				break

		return documents

	# Done
	def search(self, query):
		
		words = parse_string(query)
		
		if len(words) == 1:
			ranked_results = self.single_word_query(words[0])
			# Todo Sort
			return self.get_docs(ranked_results.keys())
		
		elif len(words) > 1:
			ranked_results = self.multi_word_query(words)
			# Todo Sort
			return self.get_docs(ranked_results.keys())

		else:
			raise Exception("Enter Valid Query")


if __name__ == "__main__":
	pass