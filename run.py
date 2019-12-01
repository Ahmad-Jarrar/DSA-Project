import time
import os


from helper.functions import *
from Lexicon import lexicon
from Indexing.ForwardIndex import forward_index
from Indexing.InvertedIndex import inverted_index

if __name__ == "__main__":

    build_paths()
    lexicon.load_lexicon(update=True)
    forward_index()
    inverted_index()
