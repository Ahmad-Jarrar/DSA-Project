import os

PROJECT_PATH = os.getcwd()


# Give the path of your dataset
DATA_PATH = os.path.join(PROJECT_PATH, 'Data')

# internal Files
FILES_PATH = os.path.join(PROJECT_PATH, 'Storage')
LEXICON_PATH = os.path.join(FILES_PATH, 'lexicon.json')

BARRELS_PATH = os.path.join(FILES_PATH, 'barrels')
FORWARD_BARRELS_PATH = os.path.join(BARRELS_PATH, 'forward_barrels')
INVERTED_BARRELS_PATH = os.path.join(BARRELS_PATH, 'inverted_barrels')

EXTRA_PATH = os.path.join(FILES_PATH, 'extra')

SHORT_BARRELS = os.path.join(FILES_PATH, 'short_barrels')
SHORT_FORWARD_BARRELS_PATH = os.path.join(SHORT_BARRELS, 'forward_barrels')
SHORT_INVERTED_BARRELS_PATH = os.path.join(SHORT_BARRELS, 'inverted_barrels')

NO_OF_THREADS = 8
# NO_OF_BARRELS = 64

BARREL_CAPACITY = 16000


def build_paths():
    """
        Run to build the environment for internal files of project
    """
    print("Creating Paths!")
    try:
        os.stat(FILES_PATH)
    except:
        os.mkdir(FILES_PATH)
    
    try:
        os.stat(BARRELS_PATH)
    except:
        os.mkdir(BARRELS_PATH)

    try:
        os.stat(FORWARD_BARRELS_PATH)
    except:
        os.mkdir(FORWARD_BARRELS_PATH)

    try:
        os.stat(INVERTED_BARRELS_PATH)
    except:
        os.mkdir(INVERTED_BARRELS_PATH)

    try:
        os.stat(SHORT_BARRELS)
    except:
        os.mkdir(SHORT_BARRELS)

    try:
        os.stat(SHORT_FORWARD_BARRELS_PATH)
    except:
        os.mkdir(SHORT_FORWARD_BARRELS_PATH)

    try:
        os.stat(SHORT_INVERTED_BARRELS_PATH)
    except:
        os.mkdir(SHORT_INVERTED_BARRELS_PATH)

    try:
        os.stat(EXTRA_PATH)
    except:
        os.mkdir(EXTRA_PATH)

if __name__ == "__main__":
    build_paths()