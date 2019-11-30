import os


PROJECT_PATH = os.getcwd()


# Give the path of your dataset
DATA_PATH = os.path.join(PROJECT_PATH, 'Data')

# internal Files
FILES_PATH = os.path.join(PROJECT_PATH, 'Storage')
LEXICON_PATH = os.path.join(FILES_PATH, 'lexicon.json')
BARRELS_PATH = os.path.join(FILES_PATH, 'barrels')


NO_OF_THREADS = 8


def build_paths():

    try:
        os.stat(FILES_PATH)
    except:
        os.mkdir(FILES_PATH)
    
    try:
        os.stat(BARRELS_PATH)
    except:
        os.mkdir(BARRELS_PATH)
