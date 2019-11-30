import time
import os


from helper.functions import *
from Lexicon import lexicon
from Indexing.ForwardIndex import index 

if __name__ == "__main__":

    build_paths()
    lexicon.load_lexicon(update=True)
    index()
