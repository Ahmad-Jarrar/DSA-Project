import time
import os

from helper.functions import *
from Lexicon import lexicon
from Indexing.ForwardIndex import forward_index
from Indexing.InvertedIndex import inverted_index
from UserInterface.UI import *

if __name__ == "__main__":
    # Build File Directories
    build_paths()

    # # Generate Forward Index for Documents in dataset
    # forward_index()

    # # Generate Inverted Index from barrels produced by forward_index
    # inverted_index()

    SearchEngineApp().run()
